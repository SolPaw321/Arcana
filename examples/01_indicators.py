"""
How to add an indicator?
"""
from arcana.indicators.interface import IndicatorData
# necessary imports
from arcana.price_data import CCTXCfg, CCTXLoader, PriceData

###                                ###
# ---| Moving Average Indicator |--- #
###                                ###

# first of all load the OHLCV data (see 00_price_data.py)
loader = CCTXLoader()
data_cfg = CCTXCfg(
    interval="1D",
    symbols=("BINANCE:ETHBTC", "BYBIT:SOLUSDT", "KRAKEN:DOGEBTC"),
    limit=1000,
)

price_data = PriceData(loader_factory=loader)
price_data.load(data_cfg=data_cfg)
print(price_data.prices)


# now we can implement some indicators
print("Alivable Indicators")
print(IndicatorData.show_supported_indicators())

# lets calculete some
from arcana.indicators.indicators import SMA, FRAMA, KAMA, SMACfg, FRAMACfg, KAMACfg
ind_data = IndicatorData(price_data)

sma_cfg = SMACfg(user_name="sma_1", src="close", period=50)
ind_data.add_moving_average(SMA, ind_config=sma_cfg)

sma_cfg = SMACfg(user_name="sma_2", src="open", period=100)
ind_data.add_moving_average(SMA, ind_config=sma_cfg)

frama_cfg = FRAMACfg(user_name="frama_1", src="close", period=20)
ind_data.add_moving_average(FRAMA, ind_config=frama_cfg)

kama_cfg = KAMACfg(user_name="kama_1", src="close", period=20, n_fast=10, n_slow=30)
ind_data.add_moving_average(KAMA, ind_config=kama_cfg)

# show all yours indicators
print("User indicators:")
ind_data.show_user_indicators()

# get the data
print(ind_data.get_ind_data("sma_1"))
print(ind_data.get_ind_data("sma_2"))
print(ind_data.get_ind_data("frama_1"))
print(ind_data.get_ind_data("kama_1"))

