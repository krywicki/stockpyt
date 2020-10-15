import argparse
from rich.table import Table
from rich.console import Console
from rich import box
from stockpyt import get_ticker, StockQuote

def display_quotes(quotes:list):
    table = Table(header_style="blue", box=box.ASCII2)

    # draw headers
    table.add_column("Symbol", style="dim", width=12)
    table.add_column("Price", justify="right", width=12)
    table.add_column("Open", justify="right", width=12)
    table.add_column("High", justify="right", width=12)
    table.add_column("Low", justify="right", width=12)
    table.add_column("Prev. Close", justify="right", width=12)
    table.add_column("% Change", justify="right", width=12)

    # draw rows
    quote:StockQuote
    for quote in quotes:
        if quote.err:
            table.add_row(quote.symbol, quote.err)
        else:
            perc_change = 0
            if quote.perc_change > 0:
                perc_change = "[green]{:.2f} %[/green]".format(quote.perc_change)
            else:
                perc_change = "[red]{:.2f} %[/red]".format(quote.perc_change)

            table.add_row(quote.symbol,
                f"${round(quote.price,2)}",
                f"${round(quote.open,2)}",
                f"${round(quote.high,2)}",
                f"${round(quote.low,2)}",
                f"${round(quote.prev_close,2)}",
                perc_change)

    console = Console()
    console.print(table)


# parse args
parser = argparse.ArgumentParser(prog="stockpyt", description="Fetches stock quotes")
parser.add_argument("symbol", help="stock symbol", nargs="*")
args = parser.parse_args()

# fetch quotes and draw
quotes = get_ticker().get_quotes(args.symbol)
display_quotes(quotes)