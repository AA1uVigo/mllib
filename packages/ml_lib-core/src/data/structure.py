import os
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DatasetStructure:
    root_dir     : str
    original_data: str = field(init=False)
    dev_split    : str = field(init=False)
    val_split    : str = field(init=False)
    dev_subsplit : str = field(init=False)
    val_subsplit : str = field(init=False)
    metadata     : str = field(init=False)

    def __post_init__(self) -> None:
        self.original_data = os.path.join(self.root_dir, "original")
        self.dev_split     = os.path.join(self.root_dir, "dev_split")
        self.val_split     = os.path.join(self.root_dir, "val_split")
        self.dev_subsplit  = os.path.join(self.dev_split, "subsplit")
        self.val_subsplit  = os.path.join(self.val_split, "subsplit")
        self.metadata      = os.path.join(self.root_dir, "metadata")

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

