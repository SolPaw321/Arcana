from tvDatafeed import Interval as tvInterval
import ccxt

from .dev_types import Interval

_TV_INTERVAL_MAP = {
    Interval.m1: tvInterval.in_1_minute,
    Interval.m3: tvInterval.in_3_minute,
    Interval.m5: tvInterval.in_5_minute,
    Interval.m15: tvInterval.in_15_minute,
    Interval.m30: tvInterval.in_30_minute,
    Interval.m45: tvInterval.in_45_minute,
    Interval.h1: tvInterval.in_1_hour,
    Interval.h2: tvInterval.in_2_hour,
    Interval.h3: tvInterval.in_3_hour,
    Interval.h4: tvInterval.in_4_hour,
    Interval.D1: tvInterval.in_daily,
    Interval.W1: tvInterval.in_weekly,
    Interval.M1: tvInterval.in_monthly,
}


def tv_interval_adapter(v):
    if v in _TV_INTERVAL_MAP:
        return _TV_INTERVAL_MAP[v]
    raise ValueError(f"Interval {v.value} is not supported in TradingView. Use {[key.value for key in _TV_INTERVAL_MAP]}")


def ccxt_symbol_adapter(v):
    exchange, ticker = v.split(":")

    if exchange.lower() in ccxt.exchanges:
        exg = getattr(ccxt, exchange.lower())()

        ticker_map = {
            tick.replace("/", ""): tick for tick in exg.load_markets()
        }

        if ticker in ticker_map:
            return exg, ticker_map[ticker]
        raise ValueError(f"Unknown ticker {ticker}.")
    raise ValueError(f"Unknown exchange {exchange}.")


def ccxt_interval_adapter(interval, exchange):
    if interval == "1D" or interval == "1W": # critical point
        interval = interval.lower()

    if interval in exchange.timeframes:
        return exchange.timeframes[interval]
    raise ValueError(f"Unknown or unsupported interval {interval}. Exchange {exchange} supports {list(exchange.timeframes.keys())}.")

