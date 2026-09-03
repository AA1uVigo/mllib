from abc import abstractmethod
from dataclasses import dataclass
from typing import Tuple, List, Dict, ClassVar

from pandas import DataFrame

from ..config import BaseConfig
from ..registry import Registry
from ..data import DatasetStructure
from ..processor import ElementalProcessor

@dataclass
class SplitConfig(BaseConfig):
    dev_split_fraction: float
    dev_subsplits: Dict[str, float]
    tst_subsplits: Dict[str, float]
    types: ClassVar[Registry[BaseSplitter]] = Registry("splitters")

class BaseSplitter(ElementalProcessor):
    def __init__(self, config: SplitConfig, dataset_structure: DatasetStructure) -> None:
        super().__init__(config, dataset_structure)

    @abstractmethod
    def split(self, data: DataFrame) -> Tuple[Tuple[DataFrame, List[DataFrame]], Tuple[DataFrame, List[DataFrame]]]:
        pass

    @abstractmethod
    def _generate_subsplits(self, data: DataFrame, subsplits: List[float]) -> List[DataFrame]:
        pass

    def step(self, data: DataFrame) -> Tuple[Tuple[DataFrame, List[DataFrame]], Tuple[DataFrame, List[DataFrame]]]:
        return self.split(data)

@SplitConfig.splitters.register()    
class RandomSplitter(BaseSplitter):
    name = "random"
    def __init__(self, split_config: SplitConfig) -> None:
        super().__init__(split_config)

    def split(self, data: DataFrame) -> Tuple[Tuple[DataFrame, List[DataFrame]], Tuple[DataFrame, List[DataFrame]]]:
        dev_fraction = self.split_config.dev_split_fraction
        dev_data = data.sample(frac=dev_fraction, random_state=42)
        tst_data = data.drop(dev_data.index)

        dev_subsplits_data = self._generate_subsplits(dev_data, list(self.split_config.dev_subsplits.values()))
        tst_subsplits_data = self._generate_subsplits(tst_data, list(self.split_config.tst_subsplits.values()))

        return (dev_data, dev_subsplits_data), (tst_data, tst_subsplits_data)

    def _generate_subsplits(self, data: DataFrame, subsplits: List[float]) -> List[DataFrame]:
        aux_data = data.copy()
        acc = 1
        subsplits_data = []
        for subsplit_fraction in subsplits:
            subsplits_data.append(aux_data.sample(frac=subsplit_fraction/acc))
            acc -= subsplit_fraction
            aux_data = aux_data.drop(subsplits_data[-1].index)
        return subsplits_data