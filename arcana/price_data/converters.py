import re
from pathlib import Path

from .dev_types import Interval


INTERVAL_ALIASES = {
    Interval.m1: ("1", "minute", "1 minute", "1m", "m1"),
    Interval.m3: ("3", "3 minutes", "3m", "m3"),
    Interval.m5: ("5", "5 minutes", "5m", "m5"),
    Interval.m15: ("15", "15 minutes", "15m", "m15"),
    Interval.m30: ("30", "30 minutes", "30m", "m30"),
    Interval.m45: ("45", "45 minutes", "45m", "m45"),
    Interval.h1: ("hour", "1 hour", "1h", "h1"),
    Interval.h2: ("2 hours", "2h", "h2"),
    Interval.h3: ("3 hours", "3h", "h3"),
    Interval.h4: ("4 hours", "4h", "h4"),
    Interval.D1: ("daily", "D1", "1D", "day", "D"),
    Interval.W1: ("weekly", "W1", "1W", "week", "W"),
    Interval.M1: ("monthly", "M1", "1M", "month", "M"),
    Interval.M3: ("quarterly", "M3", "3M", "quarter", "Q"),
    Interval.M6: ("half a year", "M6", "6M", "half", "H"),
    Interval.M12: ("yearly", "M12", "12M", "year", "R"),
}

def interval_converter(v):
    interval_map = {val: key for key, vals in INTERVAL_ALIASES.items() for val in vals}
    if v not in interval_map:
        raise ValueError(f"{v} is not a valid interval. Use: {[key.value for key in INTERVAL_ALIASES]}.")
    return interval_map[v]


def symbol_converter(symbols):
    pattern = re.compile(r"^[A-Za-z]+:[A-Za-z]+$")

    if isinstance(symbols, str):
        symbols = (symbols,)

    conv_symbols = []
    for symbol in symbols:
        symbol = re.sub(r"[\d\W]+", ":", symbol).strip(":").upper()
        if pattern.fullmatch(symbol):
            conv_symbols.append(symbol)
        else:
            print(f"{symbol} is not a valid symbol format. Use the format EXCHANGE:TICKER.")

    if conv_symbols:
        return conv_symbols
    raise ValueError(f"None of {symbols} is a valid symbol format.")

def tv_fut_contract_converter(v):
    if 0 <= v <= 2:
        return v
    raise ValueError(f"{v} is not a valid fut contract parameter. Use [0, 1, 2].")


def tv_n_bars_converter(v):
    if v <= 0:
        raise ValueError(f"{v} should be positive. Use value between 1 and 5000.")
    elif v > 5000:
        print(f"{v} is too much. Reduced to 5000.")
        v = 5000
    return v

def ccxt_limit_converter(v):
    if v <= 0:
        raise ValueError(f"{v} should be positive. Use value between 1 and 1000.")
    elif v > 1000:
        print(f"{v} is too much. Reduced to 1000.")
        v = 1000
    return v

def path_converter(v, suffix, deep_search: bool = False) -> list[Path]:
    if "." not in suffix:
        suffix = "." + suffix

    if isinstance(v, str):
        v = Path(v)

    if v.is_file():
        if v.suffix == suffix:
            return [v]
        else:
            raise IOError(f"The file hase wrong suffix. Expects {suffix}, got {v.suffix}")
    elif v.is_dir():
        if not deep_search:
            files = [f for f in v.iterdir() if v.is_file() and v.suffix == suffix]
        else:
            files = list(v.rglob(suffix))

        if files:
            return files

        if not deep_search:
            raise ValueError(f"Folder {v} does not contains any {suffix} files. Try again with deep_search=True.")
        raise ValueError(f"There is no files {suffix} linked to this folder.")
    else:
        raise IOError(f"Make sure that the folder or file {suffix} exists. Provided path {v}")
