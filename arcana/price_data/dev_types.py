from enum import StrEnum


class Interval(StrEnum):
    m1 = "1m"
    m3 = "3m"
    m5 = "5m"
    m15 = "15m"
    m30 = "30m"
    m45 = "45m"
    h1 = "1h"
    h2 = "2h"
    h3 = "3h"
    h4 = "4h"
    D1 = "1D"
    W1 = "1W"
    M1 = "1M"
    M3 = "3M"
    M6 = "6M"
    M12 = "12M"


class PriceDataColumns(StrEnum):
    DATE = "date"
    SYMBOL = "symbol"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"
