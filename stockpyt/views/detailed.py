import locale, sys, math
from typing import List
from dataclasses import dataclass

import rich
from rich.panel import Panel, Padding
from rich.console import RenderGroup, Console
from rich.table import Table, Column
from rich.text import Text
from rich.style import Style
from rich import box

from .. import StockQuote, PricePoints
from .view import View

locale.setlocale( locale.LC_ALL, '' )

@dataclass
class PriceChart:
    """
    Plot the prices on a terminal chart in a similar manner as seen below
    """

    width:int
    height:int = 10

    def _cluster_price_points(self, price_points:PricePoints) -> List[float]:
        """ cluster price point values so that they fit on the chart """

        # if price points fit on chart
        if len(price_points) <= self.width:
            return price_points

        # cluster price points to fit on chart
        pos = 0
        points = []
        cluster_size = math.ceil(len(price_points) / self.width)
        while pos < len(price_points):
            count   = 0
            val     = 0.0

            # calc average across cluster
            while count < cluster_size and pos < len(price_points):
                val += price_points[pos]
                count += 1
                pos += 1
            points.append(val/count)

        return points

    def plot(self, quote:StockQuote) -> Text:
        """ plot prices on chart """
        # grid of columns by rows
        grid = [[Text(" ", end="") for x in range(self.height)] for x in range(self.width)]
        for row in range(self.height - 1):
            grid[self.width - 1][row].end = "\n"

        high = max(quote.prev_close, quote.high)
        low = min(quote.prev_close, quote.low)
        rng = high - low

        # prev. close vertical index in chart
        pc_index = round(((quote.prev_close - low) / rng) * self.height)
        pc_index = pc_index - 1 if pc_index > 0 else 0

        # clustered price points
        points = self._cluster_price_points(quote.price_points)


        # create graph
        col=0
        for point in points:
            # price point index and color
            color = "red" if point < quote.prev_close else "green"
            index = round(((point - low) / rng) * self.height)
            index = index - 1 if index > 0 else index

            # add points to grid
            for row in range(min(index, pc_index + 1), max(index, pc_index + 1) ):
                grid[col][row].style = Style(bgcolor=color)
            col+=1

        chart = Table(show_header=False, box=None, padding=0)
        chart.columns = [Column() for _ in range(self.width)]

        for row in range(self.height-1, -1, -1):
            _row = []
            for col in range(self.width):
                _row.append(grid[col][row])
            chart.add_row(*_row)

        return chart

class DetailedTerminalView(View):
    """ Detailed Stock Quote View """

    def __init__(self):

        self.console = Console()

        self.table = Table(show_header=False, box=box.SQUARE, padding=0)
        self.table.add_column(no_wrap=True, width=35)
        self.table.add_column(width=self.console.width - 38)

    def _chart_col_width(self) -> int:
        return self.table.columns[1].width

    def _fmt_pc(self, pc:float) -> str:
        """ format percent-change """
        # format percent change
        pc_str:str = "{:.2f} %".format(pc)
        pc_str = "+" + pc_str if pc > 0 else pc_str

        # set percent change color
        pc_str = f"[green]{pc_str}[/green]" if pc > 0 else f"[red]{pc_str}[/red]"

        return pc_str

    def _render_quote(self, quote:StockQuote):

        #
        # render stock quote info
        #
        info = Table(expand=True, box=box.SIMPLE_HEAD, padding=(0, 0), border_style="bright_black")
        info.add_column(header=f"[gold1]{quote.symbol}[/gold1]")
        info.add_column(header=self._fmt_pc(quote.perc_change), justify="right")

        info.add_row(Padding("Price", (1, 0, 0, 0)), Padding(locale.currency(quote.price, grouping=True), (1, 0, 0, 0)))
        info.add_row("Open", locale.currency(quote.open, grouping=True))
        info.add_row("High", locale.currency(quote.high, grouping=True))
        info.add_row("Low", locale.currency(quote.low, grouping=True))
        info.add_row("Previous Close", locale.currency(quote.prev_close, grouping=True))

        #
        # render chart
        #
        chart = PriceChart(width=self._chart_col_width())
        self.table.add_row(info, chart.plot(quote))

    def render(self, quotes:List[StockQuote]):
        console = Console()

        for quote in quotes:
            self._render_quote(quote)

        console.print(self.table)
