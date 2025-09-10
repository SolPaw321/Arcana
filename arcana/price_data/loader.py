from abc import ABC, abstractmethod
from pandas import DataFrame, to_datetime, concat, read_csv
from collections.abc import Iterable

from arcana.price_data.cfg import CSVCfg, TradingViewCfg, CCTXCfg
from arcana.price_data.adapters import tv_interval_adapter, ccxt_symbol_adapter, ccxt_interval_adapter
from arcana.price_data.dev_types import PriceDataColumns
from arcana.utils.RegistryTree import RegistryTree

COLUMN_ORDER = {
    's': PriceDataColumns.SYMBOL,
    'o': PriceDataColumns.OPEN,
    'h': PriceDataColumns.HIGH,
    'l': PriceDataColumns.LOW,
    'c': PriceDataColumns.CLOSE,
    #'v': PriceDataColumns.VOLUME,
}
INDEX_NAME = PriceDataColumns.DATE


def _normalize_columns(df: DataFrame) -> DataFrame:
    index_name = df.index.name
    df = df.reset_index(drop=False)
    df.rename(columns={index_name: INDEX_NAME}, inplace=True)
    df = df.set_index(INDEX_NAME, drop=True)
    df.rename(columns={col[0]: COLUMN_ORDER[col[0]] for col in df.columns if col in COLUMN_ORDER}, inplace=True)
    df = df.reindex(columns=list(COLUMN_ORDER.values()))
    return df

def _create_df_from_raw_array(raw_data: DataFrame) -> DataFrame:
    df = DataFrame(raw_data, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = to_datetime(df['date'], unit="ms")
    df.set_index("date", drop=True, inplace=True)
    return df

class PriceDataLoader(ABC):
    """The main factory for loading OHLCV data."""

    __slots__ = ()
    _registry = RegistryTree("PriceData")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        bases_names =  [base.name() for base in cls.__mro__[::-1] if base not in (ABC, object)]
        for i in range(1, len(bases_names)):
            cls._registry.add_key(bases_names[i], parent=bases_names[i-1])

    @abstractmethod
    def loader(self):
        return

    @classmethod
    def name(cls):
        return cls.__name__.removesuffix("Loader")

    @classmethod
    def registered(cls):
        return cls._registry.render_tree()

class _LoaderName:
    __slots__ = ()

    @classmethod
    def name(cls):
        return cls.__name__.removeprefix("_")

class _TradingView(_LoaderName):
    """Obj for handling Trading View OHLCV data."""

    __slots__ = ('_loader_cfg',)

    def __init__(self, loader_cfg):
        self._loader_cfg = loader_cfg

    def load(self, data_cfg: TradingViewCfg) -> list[DataFrame]:
        """Loading OHLCV data from Trading View via tvDatafeed logic."""
        from tvDatafeed import TvDatafeed

        client = TvDatafeed(**self._loader_cfg)
        symbols = data_cfg.symbols
        interval = tv_interval_adapter(data_cfg.interval)
        n_bars = data_cfg.n_bars
        fut_contract = data_cfg.fut_contract
        extended_session = data_cfg.extended_session

        print("Downloading data...")
        df_ = []
        for symbol in symbols:
            print(symbol)
            df: DataFrame = client.get_hist(
                symbol=symbol,
                interval=interval,
                n_bars=n_bars,
                fut_contract=fut_contract,
                extended_session=extended_session
            )
            df = _normalize_columns(df)
            df_.append(df)
            print(df)
            from time import sleep
            sleep(1)
        return df_


class _CCTX(_LoaderName):
    """Obj for handling CCTX OHLCV data."""

    __slots__ = ()

    @staticmethod
    def load(data_cfg: CCTXCfg) -> list[DataFrame]:
        """Loading OHLCV data via CCTX logic."""

        symbols = data_cfg.symbols
        limit = data_cfg.limit

        df_ = []
        for symbol in symbols:
            exchange, ticker = ccxt_symbol_adapter(symbol)
            timeframe = ccxt_interval_adapter(data_cfg.interval, exchange)
            raw_data = exchange.fetch_ohlcv(
                symbol=ticker,
                timeframe=timeframe,
                limit=limit,
                since=None,
            )
            df = _create_df_from_raw_array(raw_data)
            df_.append(df)
        return df_


class _CSV(_LoaderName):
    """Load data via csv file."""

    __slots__ = ()

    @staticmethod
    def load(data_cfg: CSVCfg) -> list[DataFrame]:
        df_ = []
        for path in data_cfg.path:
            df = read_csv(path)

            # normalization...

            df_.append(df)

        return df_

class TradingViewLoader(PriceDataLoader):
    """The TradingView OHLCV data loader factory."""

    __slots__ = ('loader_params',)

    def __init__(self, *, username: str = None, password: str = None):
        self.loader_params = {
            "username": username,
            "password": password,
        }

    def loader(self) -> _TradingView:
        return _TradingView(self.loader_params)

class CCTXLoader(PriceDataLoader):
    """The CCTX price OHLCV loader factory."""

    __slots__ = ()

    def loader(self) -> _CCTX:
        return _CCTX()

class CSVLoader(PriceDataLoader):
    """The csv price OHLCV loader factory."""

    __slots__ = ()

    def loader(self) -> _CSV:
        return _CSV()
