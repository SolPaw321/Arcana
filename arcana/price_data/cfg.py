import attrs
from collections.abc import Iterable

from .utils.PATHS import DOWNLOADED_DATA
from .converters import *

@attrs.define(slots=True, kw_only=True)
class PriceDataCfg:
    interval = attrs.field(validator=attrs.validators.instance_of(str), converter=interval_converter)
    symbols = attrs.field(validator=attrs.validators.instance_of(str | Iterable), converter=symbol_converter)

    @property
    def name(self):
        return self.__class__.__name__.removesuffix("Cfg")

@attrs.define(slots=True, kw_only=True)
class TradingViewCfg(PriceDataCfg):
    n_bars = attrs.field(validator=attrs.validators.instance_of(int), converter=tv_n_bars_converter)
    fut_contract = attrs.field(default=0, validator=attrs.validators.instance_of(int), converter=tv_fut_contract_converter)
    extended_session = attrs.field(default=False, validator=attrs.validators.instance_of(bool))


@attrs.define(slots=True, kw_only=True)
class CCTXCfg(PriceDataCfg):
    limit = attrs.field(validator=attrs.validators.instance_of(int), converter=ccxt_limit_converter)
    # since = attrs.field()

@attrs.define(slots=True, kw_only=True)
class CSVCfg(PriceDataCfg):
    suffix = attrs.field(validator=attrs.validators.instance_of(str), default=".csv")
    deep_search = attrs.field(validator=attrs.validators.instance_of(bool), default=False)
    path = attrs.field(validator=attrs.validators.instance_of(str | Path), default=DOWNLOADED_DATA)

    def __attrs_post_init__(self):
        self.path = path_converter(self.path, self.suffix, self.deep_search)
