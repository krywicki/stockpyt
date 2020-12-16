from typing import List, Any
import sys, requests

from .common import TickerAgent, StockQuote, PricePoints
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
        quote.high          = max(self._as_price_points(indicators['high']))
        quote.low           = min(self._as_price_points(indicators['low']))
        quote.prev_close    = meta['previousClose']
        quote.price         = meta['regularMarketPrice']
        quote.perc_change   = -((quote.prev_close - quote.price) / quote.prev_close) * 100.0
        quote.price_points  = self._as_price_points(indicators['open'])

        return quote

    def _as_price_points(self, values:list) -> PricePoints:
        """ convert list of prices to pricepoints """
        points = PricePoints()

        for val in values:
            if isinstance(val, list):
                points.append(self._as_price_points(val))

            elif not val:
                continue

            else:
                points.append(val)

        return points
