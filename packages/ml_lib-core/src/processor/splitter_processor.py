from abc import abstractmethod

from typing import Tuple, List, Dict

from pandas import DataFrame

from ..data import DatasetStructure
from ..config import SplitConfig, SPLITTER_REGISTRY
from ..processor import ElementalProcessor

class BaseSplitter(ElementalProcessor):
    def __init__(self, config: SplitConfig, dataset_structure: DatasetStructure) -> None:
        super().__init__(config, dataset_structure)
        dataset_structure.add_subsplits(config.dev_subsplits, config.tst_subsplits)

    @abstractmethod
    def split(self, data: DataFrame) -> Tuple[Tuple[DataFrame, List[DataFrame]], Tuple[DataFrame, List[DataFrame]]]:
        pass

    @abstractmethod
    def _generate_subsplits(self, data: DataFrame, subsplits: Dict[float]) -> Dict[DataFrame]:
        pass

    def step(self, data: DataFrame) -> Tuple[Tuple[DataFrame, Dict[DataFrame]], Tuple[DataFrame, Dict[DataFrame]]]:
        splits = self.split(data)
        with open(self.dataset_structure.dev_split + "/base.csv", "w") as file:
            splits[0][0].to_csv(file, index=False)
        with open(self.dataset_structure.tst_split + "/base.csv", "w") as file:
            splits[1][0].to_csv(file, index=False)

        for name, subsplit_data in splits[0][1].items():
            with open(self.dataset_structure.dev_subsplit_list[name] + "/base.csv", "w") as file:
                subsplit_data.to_csv(file)
        for name, subsplit_data in splits[1][1].items():
            with open(self.dataset_structure.tst_subsplit_list[name] + "/base.csv", "w") as file:
                subsplit_data.to_csv(file)
        return splits

@SPLITTER_REGISTRY.register()
class RandomSplitter(BaseSplitter):
    name = "random"
    def __init__(self, split_config: SplitConfig, dataset_structure: DatasetStructure) -> None:
        super().__init__(split_config, dataset_structure)

    def split(self, data: DataFrame) -> Tuple[Tuple[DataFrame, Dict[DataFrame]], Tuple[DataFrame, Dict[DataFrame]]]:
        dev_fraction = self.config.dev_split_fraction
        dev_data = data.sample(frac=dev_fraction, random_state=42)
        tst_data = data.drop(dev_data.index)

        dev_subsplits_data = self._generate_subsplits(dev_data, self.config.dev_subsplits)
        tst_subsplits_data = self._generate_subsplits(tst_data, self.config.tst_subsplits)

        return (dev_data, dev_subsplits_data), (tst_data, tst_subsplits_data)

    def _generate_subsplits(self, data: DataFrame, subsplits: Dict[float]) -> Dict[DataFrame]:
        aux_data = data.copy()
        acc = 1
        subsplits_data = {}
        for name, subsplit_fraction in subsplits.items():
            subsplits_data[name] = aux_data.sample(frac=subsplit_fraction/acc)
            acc -= subsplit_fraction
            aux_data = aux_data.drop(subsplits_data[name].index)
        return subsplits_data