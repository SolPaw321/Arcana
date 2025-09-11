from pandas import DataFrame

from . import PriceDataColumns
from .loader import PriceDataLoader
from .cfg import PriceDataCfg
from arcana.utils.df_utils import stack_data
from arcana.utils.classes_utils import validate_classes_names
from arcana.plotter import Plotter

class PriceData:
    """The main obj for handling price data"""

    __slots__ = ('loader', '_prices', "_data_cfg")

    def __init__(self, loader_factory: PriceDataLoader):
        self.loader = loader_factory.loader()
        validate_classes_names(loader_factory.name(), self.loader.name())

        self._prices = None
        self._data_cfg = None

    def load(self, data_cfg: PriceDataCfg) -> DataFrame:
        validate_classes_names(self.loader.name(), data_cfg.name)
        self._data_cfg = data_cfg
        self._prices = self.loader.load(self._data_cfg)
        return stack_data(self._prices, self._data_cfg.symbols)

    @property
    def prices_raw(self) -> list[DataFrame]:
        return self._prices

    @property
    def prices(self) -> DataFrame:
        return stack_data(self._prices, self._data_cfg.symbols)

    @property
    def data_cfg(self) -> PriceDataCfg:
        return self._data_cfg

    @staticmethod
    def get_registered_loaders():
        return PriceDataLoader.registry.all_registered()

    @staticmethod
    def show_registered_loaders():
        PriceDataLoader.registry.render_tree()

    def plot(self):
        plotter = Plotter(rows=1, cols=1, row_heights=[1.0], subplot_titles=self.data_cfg.symbols)