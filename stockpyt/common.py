from typing import List
from pprint import pformat

from . import tickers
from .errors import StockpytError

class StockQuote:
    """ Object that represents stock """
    def __init__(self):
        self.symbol:str         = ""
        self.high:float         = 0.0
        self.low:float          = 0.0
        self.open:float         = 0.0
        self.price:float        = 0.0
        self.perc_change:float  = 0.0   # percent change from prev close
        self.prev_close:float   = 0.0   # previous close
        self.err:str            = ""

    @classmethod
    def from_err(cls, symbol:str, err:str):
        c = cls()
        c.symbol = symbol
        c.err = err
        return c

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self.err:
            return pformat({
                "symbol": self.symbol,
                "err"   : self.err
            })
        else:
            return pformat({
                "symbol": self.symbol,
                "high"  : f"${round(self.high,2)}",
                "low"   : f"${round(self.low,2)}",
                "open"  : f"${round(self.open,2)}",
                "price" : f"${round(self.price,2)}",
                "percent change" : "{:.2f}%".format(self.perc_change),
                "pervious close" : f"${round(self.prev_close,2)}"
            })

class TickerAgent:
    """ Ticker Agent for retrieving stock data """

    def get_quotes(self, symbols:List[str]) -> List[StockQuote]:
        """ Gets stock quote by symbol
        -symbols: one or more stock symbols
        returns: List of stock quotes
        """
        raise NotImplementedError

def get_ticker() -> TickerAgent:
    """ get default ticker agent """
    return tickers.YahooTickerAgent()
