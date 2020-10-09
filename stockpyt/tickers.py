from typing import List, Any
import requests

from .common import TickerAgent, QuoteResult, StockQuote
from .errors import StockpytError

class YahooTickerAgent(TickerAgent):
    """ Yahoo Ticker Agent """

    def get_quote_url(self, symbol:str) -> str:
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"\
            "?region=USincludePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

    def get_quotes(self, symbols:List[str]) -> List[QuoteResult]:
        """ Get stock quotes, by symbol, from yahoo finance """
        results:List[QuoteResult] = []
        for symbol in symbols:
            results.append(self._get_quote(symbol))
        return results

    def _get_quote(self, symbol:str) -> QuoteResult:
        resp = requests.get(self.get_quote_url(symbol))
        if resp.status_code == 200:
            quote = self._parse_resp(resp)
            return QuoteResult.from_ok(quote)
        else:
            return QuoteResult.from_bad("bad request")

    def _parse_resp(self, resp=requests.Response) -> StockQuote:
        data = resp.json()

        meta       = data['chart']['result'][0]['meta']
        indicators = data['chart']['result'][0]['indicators']['quote'][0]

        quote               = StockQuote()
        quote.symbol        = meta['symbol']
        quote.open          = indicators['open'][0]
        quote.high          = max(indicators['high'])
        quote.low           = min(indicators['low'])
        quote.prev_close    = meta['previousClose']
        quote.price         = meta['regularMarketPrice']
        quote.perc_change   = ((quote.prev_close - quote.price) / quote.prev_close) * 100.0

        return quote