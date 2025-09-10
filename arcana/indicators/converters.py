from arcana.price_data.dev_types import PriceDataColumns

OHLC_ALIES = {
    PriceDataColumns.OPEN: ('open', 'o'),
    PriceDataColumns.HIGH: ('high', 'h'),
    PriceDataColumns.LOW: ('low', 'l'),
    PriceDataColumns.CLOSE: ('close', 'c'),
}

def src_converter(v):
    inv_alies = {val: key for key, vals in OHLC_ALIES.items() for val in vals}
    if v in inv_alies:
        return inv_alies[v]
    raise ValueError(f"{v} is not valid src. Use {[al.value for al in OHLC_ALIES.keys()]}")

