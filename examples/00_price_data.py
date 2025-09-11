"""
How to load OHLCV data?
"""
# necessary imports
from arcana.price_data import TradingViewLoader, CCTXLoader, TradingViewCfg, CCTXCfg, PriceData

###                                                         ###
# ---| Downloading data from Trading View via tvDatafeed |--- #
###                                                         ###

# specify the Trading View loader
# you can use your real account
loader = TradingViewLoader(username=None, password=None)

print("Alivable loader:")
PriceData.show_registered_loaders()

# specify the OHLCV cata configuration
data_cfg = TradingViewCfg(
    interval="1D",                                 # the interval
    symbols=("INDEX:ETHUSD", "INDEX:BTCUSD"),      # EXCHANGE:SYMBOL to download
    n_bars=1000,                                   # the last n bars (candles)
)

# define the price data interface...
price_data = PriceData(loader_factory=loader)

# ... and load the data
price_data.load(data_cfg=data_cfg)

# now you can display your raw data
raw_data = price_data.prices_raw
print(raw_data)

# you can also stack raw data
data = price_data.prices
print(data)



###                                                         ###
# ---| Downloading data from ByBit and Binance via CCXT |--- #
###                                                         ###


# specify ccxt loader
loader = CCTXLoader()

# specify OHLCV data configuration
data_cfg = CCTXCfg(
    interval="1D",
    symbols=("BINANCE:ETHUSDT", "BYBIT:BTCUSDT", "BINANCE:ETHBTC"),
    limit=1000,
)

# define the price data interface...
price_data = PriceData(loader_factory=loader)

# ... and load the data
price_data.load(data_cfg=data_cfg)

# now you can display your raw data
raw_data = price_data.prices_raw
print(raw_data)

# you can also stack raw data
data = price_data.prices
print(data)