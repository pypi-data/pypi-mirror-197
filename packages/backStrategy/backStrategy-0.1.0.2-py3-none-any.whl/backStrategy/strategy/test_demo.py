# -*- coding: utf-8 -*-
# @Time    : 2022/10/28
# @Author  : 邓大大
# @Desc    : 根据交易量判断交易点 V2.
from typing import List

from backStrategy.engine.template import CtaTemplate
from backStrategy.utils.object import BarData


class TestDemo(CtaTemplate):
    stop_profit_rate = 0.01
    stop_loss_rate = 0.01

    def __init__(self, cta_engine, strategy_name, symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, symbol, setting)

        self.line_chart: dict = {}  # {"2020-01-01 00:00:00": -1, "2020-02-02 01:00:00": -0.5, "2020-03-03 02:00:00": 0}
        self.line_table: list = [["信号时间", "开仓价", "开仓时间", "止盈价", "止损价", "信号结束时间(平仓)", "结果"]]
        self.detail_dict: dict = {"总信号": 0, "胜利": 0, "失败": 0}

        self.one_result = {"信号时间": "",
                           "开仓价": 0.0,
                           "开仓时间": "",
                           "止盈价": 0.0,
                           "止损价": 0.0,
                           "信号结束时间(平仓)": "",
                           "结果": ""
                           }

        self.signal: bool = False  # 是否找到信号
        self.open_pos: bool = False  # 是否开仓

        self.am: List[BarData] = []
        self.am30 = []
        self.am7 = []

    def on_start(self):
        print("策略开始")

    def on_stop(self):
        print("策略停止")
        print(self.line_chart)

    def on_bar(self, bar: BarData):
        """
        K 线推送，按时间先后顺序.
        """
        # 判断是否找到开仓信号,
        # 若果没有找到，寻找信号
        print(bar)
        if not self.signal:
            self.find_signal(bar)
        else:
            # 判断是否开仓了，如果开仓了就开始判断止盈止损，否则开仓
            if self.open_pos:
                stop = self.handle_profit_loss(self.one_result["止盈价"], self.one_result["止损价"], bar)
                if stop:
                    # 如果止盈止损了, 将这次信号的所有结果，记录下来
                    self.add_result()
            else:
                self.buy(bar)

    def add_result(self):
        """每次信号结束，记录结果"""
        self.line_table.append([v for k, v in self.one_result.items()])

        # 模仿利润
        self.line_chart[self.one_result['信号结束时间(平仓)']] = -1 if self.one_result['结果'] == "止盈" else 1

        # 初始化每次结果
        self.one_result = {"信号时间": "",
                           "开仓价": 0.0,
                           "开仓时间": "",
                           "止盈价": 0.0,
                           "止损价": 0.0,
                           "信号结束时间(平仓)": "",
                           "结果": "",
                           }
        self.signal = False
        self.open_pos = False

    def buy(self, bar: BarData):
        """开仓, 并且计算止盈止损"""
        self.open_pos = True
        self.one_result['开仓价'] = bar.open_price
        self.one_result['开仓时间'] = str(bar.datetime)

        self.one_result['止盈价'] = bar.open_price * (1 + self.stop_profit_rate)
        self.one_result['止损价'] = bar.open_price * (1 - self.stop_loss_rate)

    def find_signal(self, bar: BarData):
        """处理策略主要逻辑： 计算双均线，寻找金叉死叉, 金叉做多, 死叉做空"""

        #  计算双均线
        if len(self.am) >= 30:
            del self.am[0]

        self.am.append(bar)

        if len(self.am) < 30:
            return

        self.am30.append(sum([b.close_price for b in self.am]) / 30)
        self.am7.append(sum([b.close_price for b in self.am[24:]]) / 7)

        # 寻找金叉死叉
        if len(self.am30) > 1:
            if self.am7[-1] < self.am30[-1]:
                print("死叉, 死叉做多")
                self.one_result["信号时间"] = str(bar.datetime)  # 将信号时间添加到 当前信号结果中
                self.signal = True

    def handle_profit_loss(self, stop_profit_price: float, stop_loss_price: float, bar: BarData):
        """
        判断止盈止损
        :param stop_profit_price: 止盈价
        :param stop_loss_price: 止损价
        :param bar: k线
        """
        # 如果止盈价 < 最高价
        if stop_profit_price < bar.high_price:
            # 止损价 < 最低价
            if stop_loss_price < bar.low_price:
                # 止盈了
                self.stop_profit_open(bar)
                return True
            else:
                # 止损了
                self.stop_loss_open(bar)
                return True
        elif stop_loss_price > bar.low_price:
            # 止损了
            self.stop_loss_open(bar)
            return True
        return False

    def stop_profit_open(self, bar: BarData):
        self.detail_dict['总信号'] += 1
        self.detail_dict['胜利'] += 1
        self.one_result["信号结束时间(平仓)"] = str(bar.datetime)
        self.one_result['结果'] = '止盈'

    def stop_loss_open(self, bar: BarData):
        self.detail_dict['总信号'] += 1
        self.detail_dict['失败'] += 1
        self.one_result["信号结束时间(平仓)"] = str(bar.datetime)
        self.one_result['结果'] = '止损'


def start():
    from backStrategy.main import back_tester
    param = {}
    back_tester.start_strategy(strategy_class=TestDemo,
                               token="1INCH-USDT",
                               start_time="2022-01-01",
                               end_time="2022-02-01",
                               param=param,
                               file_name=[
                                   "/Users/denghui/Desktop/backStrategy/OKEX_DATA_FILE/1INCH/SPOT/1m/2022-01-01 00:00:00.xlsx"])


if __name__ == '__main__':
    start()