from datetime import datetime, timedelta
from typing import Callable
from typing import Type, Dict, List
from backStrategy.engine.template import CtaTemplate
from backStrategy.utils.object import BarData, Interval
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line, Page
from pyecharts.components import Table

INTERVAL_DELTA_MAP: Dict[Interval, timedelta] = {
    Interval.TICK: timedelta(milliseconds=1),
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta(days=1),
}


class BacktestingEngine:
    """"""

    def __init__(self) -> None:
        """"""
        self.symbol: str = ""
        self.start: datetime = None
        self.end: datetime = None
        self.strategy_class: Type[CtaTemplate] = None
        self.strategy: CtaTemplate = None
        self.bar: BarData

        self.interval: Interval = None
        self.callback: Callable = None
        self.history_data: List[BarData] = []

    def set_parameters(
            self,
            symbol: str,  # 代币类型
            start: datetime,  # 开始时间
            end: datetime = None,  # 结束时间
            interval: Interval = Interval.MINUTE,  # K线 间隔
    ):
        self.symbol = symbol
        self.interval = interval
        self.start = start
        self.end = end

    def add_strategy(self, strategy_class: Type[CtaTemplate], setting: dict) -> None:
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, self.symbol, setting
        )

    def remove_data(self, bar: BarData):
        if self.start <= bar.datetime <= self.end:
            return True
        else:
            return False

    def load_data(self, file_name: list) -> None:
        """"""
        print("开始加载历史数据")
        if self.start >= self.end:
            return

        self.history_data.clear()  # 清除之前加载的历史数据

        self.load_bar_data(
            file_name,
            self.symbol,
            self.interval
        )
        print("加载历史数据完成")

    def run_backtesting(self) -> None:
        """"""
        self.strategy.on_start()

        # Use the rest of history data for running backtesting
        for data in self.history_data:
            try:
                self.new_bar(data)
            except Exception:
                return

        self.strategy.on_stop()

        self.front_web(self.strategy.line_chart,
                       self.strategy.line_table,
                       self.strategy.detail_dict
                       )

    def line_markpoint(self, chart) -> Line:
        try:
            x = [x for x, _ in chart.items()]
            y = [x for _, x in chart.items()]
            line = (
                Line(init_opts=opts.InitOpts(width="100%", ))
                    .add_xaxis(xaxis_data=x)
                    .add_yaxis(
                    series_name='',
                    y_axis=y
                )
            )
            return line
        except Exception as e:
            print(f"折线图生产异常: {repr(e)}, chart: {chart}")
            return None

    def table_point(self, table_data: list, info: dict) -> Table:
        try:
            table = (
                Table().add(
                    table_data[0],
                    table_data[1:],
                    {"class": "fl-table", "style": "width: 100%"}
                ).set_global_opts({"title": str(info),
                                   "title_style": "style='color:red', align='center'",
                                   })
            )
            return table
        except Exception as e:
            print(f"表格生成异常: {repr(e)}, table_data: {table_data}, info: {info}")
            return None

    def front_web(self, chart: dict, table: List[list], info: dict):
        """生成前端页面"""
        page = Page()
        html_chart = self.line_markpoint(chart)
        html_table = self.table_point(table, info)
        if html_table and html_chart:
            page.add(
                html_chart,
                html_table,
            )
        elif html_chart:
            page.add(
                html_chart,
            )
        elif html_table:
            page.add(
                html_table,
            )
        else:
            return
        page.render("web_result.html")

    def new_bar(self, bar: BarData):
        """"""
        self.bar = bar
        self.strategy.on_bar(bar)

    def read_file(self, path, symbol, interval: Interval):
        data = pd.read_excel(path)  # reading file
        train_data = np.array(data)
        train_data_list: list = train_data.tolist()
        train_data_list.reverse()
        for data in train_data_list:
            bar = BarData(
                symbol=symbol,
                datetime=data[1],
                interval=interval,
                volume=float(data[3]),
                turnover=float(data[4]),
                open_price=float(data[5]),
                high_price=float(data[6]),
                low_price=float(data[7]),
                close_price=float(data[8])
            )
            if self.remove_data(bar):
                self.history_data.append(bar)
        return train_data_list

    def load_bar_data(
            self,
            file_list: List[str],
            symbol: str,
            interval: Interval
    ):
        for path in file_list:
            self.read_file(path, symbol, interval)
