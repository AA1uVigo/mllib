from dataclasses import dataclass
from typing import Dict, ClassVar

from .config_schema import BaseConfig
from ..registry import Registry, InstanceGenerator

SPLITTER_REGISTRY = Registry("splitters")
InstanceGenerator().add_registry(SPLITTER_REGISTRY)

@dataclass
class SplitConfig(BaseConfig):
    dev_split_fraction: float
    dev_subsplits: Dict[str, float]
    tst_subsplits: Dict[str, float]
    family_name: ClassVar[str] = "splitters"