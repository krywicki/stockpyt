from typing import List, Any
import requests

from .common import TickerAgent, StockQuote
from .errors import StockpytError

class YahooTickerAgent(TickerAgent):
    """ Yahoo Ticker Agent """

    def get_quote_url(self, symbol:str) -> str:
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"\
            "?region=USincludePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

    def get_quotes(self, symbols:List[str]) -> List[StockQuote]:
        """ Get stock quotes, by symbol, from yahoo finance """
        results:List[StockQuote] = []
        for symbol in symbols:
            results.append(self._get_quote(symbol))
        return results

    def _get_quote(self, symbol:str) -> StockQuote:
        resp = requests.get(self.get_quote_url(symbol))
        if resp.status_code == 200:
            return self._parse_resp(resp)
        else:
            return StockQuote.from_err(symbol, "bad request")

    def _parse_resp(self, resp=requests.Response) -> StockQuote:
        data = resp.json()

        meta       = data['chart']['result'][0]['meta']
        indicators = data['chart']['result'][0]['indicators']['quote'][0]

        quote               = StockQuote()
        quote.symbol        = meta['symbol']
        quote.open          = indicators['open'][0]
        quote.high          = self._max(indicators['high'])
        quote.low           = self._min(indicators['low'])
        quote.prev_close    = meta['previousClose']
        quote.price         = meta['regularMarketPrice']
        quote.perc_change   = -((quote.prev_close - quote.price) / quote.prev_close) * 100.0

        return quote

    def _max(self, values:list) -> float:
        """ gets max value. accounts for list-of-lists """
        val:float = 0.0
        if not values:
            return 0.0
        elif isinstance(values[0], list):
            values = [ self._max(vals) for vals in values ]

        max_val = 0.0
        for val in values:
            if isinstance(val, int) or isinstance(val, float):
                max_val = max(val, max_val)
        return max_val

    def _min(self, values:list) -> float:
        """ gets max value. accounts for list-of-lists """
        val:float = 0.0
        if not values:
            return 0.0
        elif isinstance(values[0], list):
            values = [ self._min(vals) for vals in values ]

        min_val = 0.0
        for val in values:
            if isinstance(val, int) or isinstance(val, float):
                min_val = max(val, min_val)
        return min_val

