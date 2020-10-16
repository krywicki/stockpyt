import argparse
import locale
from rich.table import Table
from rich.console import Console
from rich import box
from stockpyt import get_ticker, StockQuote

locale.setlocale( locale.LC_ALL, '' )

COL_WIDTH = 15

def draw_row(table:Table, quote:StockQuote):
    if quote.err:
        table.add_row(quote.symbol, quote.err)
        return

    #percent change
    pc:str = ""
    pc_len:int = 0

    if quote.perc_change > 0:
        pc = f"+{round(quote.perc_change,2)} %"

    elif quote.perc_change < 0:
        pc = f"{round(quote.perc_change,2)} %"

    else:
        pc = "0.00 %"

    pc_len = len(pc)
    pc = f"[green]{pc}[/green]" if quote.perc_change > 0 else f"[red]{pc}[/red]"

    pad_len = COL_WIDTH - len(quote.symbol) - pc_len
    pc_pad = "".ljust(pad_len)

    table.add_row(
        "{}{}{}".format(quote.symbol, pc_pad, pc),
        locale.currency(quote.price, grouping=True),
        locale.currency(quote.open, grouping=True),
        locale.currency(quote.high, grouping=True),
        locale.currency(quote.low, grouping=True),
        locale.currency(quote.prev_close, grouping=True))


def draw_quotes(quotes:list):
    table = Table(header_style="blue", box=box.ASCII2)

    # draw headers
    table.add_column("Symbol", width=COL_WIDTH)
    table.add_column("Price", justify="right", width=COL_WIDTH)
    table.add_column("Open", justify="right", width=COL_WIDTH)
    table.add_column("High", justify="right", width=COL_WIDTH)
    table.add_column("Low", justify="right", width=COL_WIDTH)
    table.add_column("Prev. Close", justify="right", width=COL_WIDTH)


    # draw rows
    quote:StockQuote
    for quote in quotes:
        draw_row(table, quote)
    console = Console()
    console.print(table)

# parse args
parser = argparse.ArgumentParser(prog="stockpyt", description="Fetches stock quotes")
parser.add_argument("symbol", help="stock symbol", nargs="*")
args = parser.parse_args()

# fetch quotes and draw
quotes = get_ticker().get_quotes(args.symbol)
draw_quotes(quotes)
