from abc import ABC
from typing import Any
from backStrategy.utils.object import BarData


class CtaTemplate(ABC):
    """"""
    parameters: list = []

    def __init__(
        self,
        cta_engine: Any,
        strategy_name: str,
        symbol: str,
        setting: dict,
    ) -> None:
        self.cta_engine: "CtaEngine" = cta_engine
        self.strategy_name: str = strategy_name
        self.symbol: str = symbol
        self.inited: bool = False
        self.update_setting(setting)

        self.line_chart: dict = {}  # {"2020-01-01 00:00:00": -1, "2020-02-02 01:00:00": -0.5, "2020-03-03 02:00:00": 0}
        self.line_table: list = []  # [["开盘价", "止损价", "盈利"], [3232,323,432], [23,23,32]
        self.detail_dict: dict = {}  # {"总信号": 50, "胜利": 40, "失败": 10}

    def update_setting(self, setting: dict) -> None:
        for name in self.parameters:
            if name in setting:
                setattr(self, name, setting[name])

    def on_start(self) -> None:
        pass

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_stop(self):
        pass

