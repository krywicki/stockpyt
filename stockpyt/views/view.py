from typing import List
from .. import StockQuote

class View(object):
    """ Base View Class """

    def render(self, quotes:List[StockQuote]):
        raise NotImplementedError
