from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Interval(Enum):
    MINUTE = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"

    HOUR = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"

    DAILY = "1d"
    DAILY_3 = "3d"

    WEEKLY = "1w"
    MONTH = "1M"

    TICK = "tick"


@dataclass
class BarData:
    symbol: str
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
