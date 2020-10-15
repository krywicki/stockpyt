from typing import Any
from pprint import pformat

class StockpytError(Exception):
    """ Stockpyt Error """

    def __init__(self, summary:str, detail:Any=None):
        self.summary:str    = summary
        self.detail:Any     = detail

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return pformat({
            "summary": self.summary,
            "detail": self.detail
        })
