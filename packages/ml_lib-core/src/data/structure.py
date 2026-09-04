import os

from dataclasses import dataclass, field
from typing import List, Dict

from ..config import SplitConfig

@dataclass
class DatasetStructure:
    root_dir         : str
    original_data    : str = field(init=False)
    dev_split        : str = field(init=False)
    tst_split        : str = field(init=False)
    dev_subsplit     : str = field(init=False)
    tst_subsplit     : str = field(init=False)
    metadata         : str = field(init=False)
    dev_subsplit_list: Dict[str, str] = field(default_factory=dict)
    tst_subsplit_list: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.original_data = os.path.join(self.root_dir, "original")
        self.dev_split     = os.path.join(self.root_dir, "dev_split")
        self.tst_split     = os.path.join(self.root_dir, "tst_split")
        self.dev_subsplit  = os.path.join(self.dev_split, "subsplits")
        self.tst_subsplit  = os.path.join(self.tst_split, "subsplits")
        self.metadata      = os.path.join(self.root_dir, "metadata")

    def add_subsplits(self, split_config: SplitConfig) -> None:
        self.dev_subsplit_list = {name: os.path.join(self.dev_subsplit, name) for name in split_config.dev_subsplits.keys()}
        self.tst_subsplit_list = {name: os.path.join(self.tst_subsplit, name) for name in split_config.tst_subsplits.keys()}

@dataclass
class MetadataStructure:
    name       : str
    description: str
    source     : str
    last_update: str
    variables  : Dict[str, str]
    labels     : List[str]
    features   : List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.features = [var for var in self.variables if var not in self.labels]