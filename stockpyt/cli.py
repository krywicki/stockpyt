import argparse
from stockpyt import get_ticker, StockQuote
from .views import SimpleTerminalView, DetailedTerminalView


def main():
    # parse args
    parser = argparse.ArgumentParser(prog="stockpyt", description="Fetches stock quotes")
    parser.add_argument("symbol", help="stock symbol", nargs="*")
    args = parser.parse_args()

    # fetch quotes and draw
    quotes = get_ticker().get_quotes(args.symbol)

    # simple render
    #SimpleTerminalView().render(quotes)
    DetailedTerminalView().render(quotes)
