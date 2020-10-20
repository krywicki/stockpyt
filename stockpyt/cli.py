import argparse
import locale
from rich.table import Table
from rich.console import Console
from rich import box

from stockpyt import get_ticker, StockQuote

locale.setlocale( locale.LC_ALL, '' )

COL_WIDTH = 15

def draw_row(table:Table, quote:StockQuote, style:str=None):
    if quote.err:
        table.add_row(quote.symbol, quote.err, style=style)
        return

    # format percent change
    pc:str = "{:.2f} %".format(quote.perc_change)
    pc = "+" + pc if quote.perc_change > 0 else pc
    pc_len:int = len(pc)

    # set percent change color
    pc = f"[green]{pc}[/green]" if quote.perc_change > 0 else f"[red]{pc}[/red]"
    pad_len = COL_WIDTH - len(quote.symbol) - pc_len

    table.add_row(
        "{}{}{}".format(quote.symbol, "".ljust(pad_len), pc),
        locale.currency(quote.price, grouping=True, ),
        locale.currency(quote.open, grouping=True),
        locale.currency(quote.high, grouping=True),
        locale.currency(quote.low, grouping=True),
        locale.currency(quote.prev_close, grouping=True),
        style=style)


def draw_quotes(quotes:list):
    console = Console()
    table = Table(header_style="blue", box=box.ASCII2)

    # draw headers
    table.add_column("Symbol", no_wrap=True, width=COL_WIDTH)
    table.add_column("Price", justify="right", no_wrap=True, width=COL_WIDTH)
    table.add_column("Open", justify="right", no_wrap=True, width=COL_WIDTH)
    table.add_column("High", justify="right", no_wrap=True, width=COL_WIDTH)
    table.add_column("Low", justify="right", no_wrap=True, width=COL_WIDTH)
    table.add_column("Prev. Close", justify="right", no_wrap=True, width=COL_WIDTH)

    # draw rows
    odd_row = False
    for quote in quotes:
        draw_row(table, quote, style="bright_black" if odd_row else None)
        odd_row = not odd_row
    console.print(table)

def main():
    # parse args
    parser = argparse.ArgumentParser(prog="stockpyt", description="Fetches stock quotes")
    parser.add_argument("symbol", help="stock symbol", nargs="*")
    args = parser.parse_args()

    # fetch quotes and draw
    quotes = get_ticker().get_quotes(args.symbol)
    draw_quotes(quotes)
