import argparse
from pprint import pprint
import stockpyt


def get_quotes(args):
    ticker = stockpyt.get_ticker()
    resps = ticker.get_quotes(args.symbol)
    for resp in resps:
        print(resp)

parser = argparse.ArgumentParser(prog="stockpyt", description="Fetches stock quotes")
parser.add_argument("symbol", help="stock symbol", nargs="*")
args = parser.parse_args()
get_quotes(args)

