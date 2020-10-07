from typing import List, Any
import requests
from .errors import StockpytError

class StockQuote:
    """ Object that represents stock """
    def __init__(self):
        self.symbol:str         = ""
        self.high:float         = 0.0
        self.low:float          = 0.0
        self.open:float         = 0.0
        self.price:float        = 0.0
        self.prec_change:float  = 0.0
        self.prev_close:float   = 0.0

    @property
    def is_error(self) -> bool:
        """ if stock quote error """
        return False

    def as_error(self) -> StockpytError:
        """ return as error """
        return None

class QuoteResult:
    """ Quote Result """
    def __init__(self):
        self.quote:StockQuote   = None
        self.err:str            = None

    @classmethod
    def from_ok(cls, quote:StockQuote):
        """ Construct OK Quote Result """
        c = cls()
        c.quote = quote
        return c

    @classmethod
    def from_bad(cls, err:str):
        """ Construct Bad Quote Result """
        c = cls()
        c.err = err
        return c

class TickerAgent:
    """ Ticker Agent for retrieving stock data """

    def get_quotes(self, symbols:List[str]) -> List[QuoteResult]:
        """ Gets stock quote by symbol
        -symbols: one or more stock symbols
        returns: List of stock quotes
        """
        raise NotImplementedError

class YahooTickerAgent(TickerAgent):
    """ Yahoo Ticker Agent """
    _URL =  "https://query1.finance.yahoo.com/v8/finance/chart/PLUG"\
            "?region=USincludePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

    def get_quotes(self, symbols:List[str]) -> List[QuoteResult]:
        """ Get stock quotes, by symbol, from yahoo finance """
        results:List[QuoteResult] = []
        for symbol in symbols:
            results.append(self._get_quote(symbol))
        return results

    def _get_quote(self, symbol:str) -> QuoteResult:
        resp = requests.get(self._URL)
        if resp.status_code == 200:
            quote = self._parse_resp(resp)
            return QuoteResult.from_ok(quote)
        else:
            return QuoteResult.from_bad("bad request")

    def _parse_resp(self, resp=requests.Response) -> StockQuote:
        data = resp.json()

        meta       = data['chart']['result']['meta']
        indicators = data['chart']['result']['indicators']['quote']

        quote               = StockQuote()
        quote.symbol        = data['symbol']
        quote.open          = indicators['open'][0]
        quote.high          = max(indicators['high'])
        quote.low           = min(indicators['low'])
        quote.prev_close    = meta['previousClose']
        quote.price         = meta['regularMarketPrice']

        old_price:float     = indicators['close'][-2] if len(indicators['close']) > 1 else meta['previousClose']
        new_price:float     = indicators['close'][-1]
        quote.prec_change   = ((old_price - new_price) / old_price) * 100.0

        return quote