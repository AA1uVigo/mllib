from dataclasses import dataclass
from types import Tuple, List, Dict

@dataclass
class SourceData:
    path: str
    name: str
    description: str
    data_types: Dict[str, str]

@dataclass
class SplitConfig:
    source_data: SourceData
    dev_split_fraction: float
    dev_subsplits: Dict[str, float]
    tst_subsplits: Dict[str, float]

@dataclass
class BaseConfig:
    process_id: str
    labels: List[str]
    features: List[str]

@dataclass
class StepConfig:
    name: str
    process_config: BaseConfig
    discard_after: bool = False

@dataclass
class ProcessConfig:
    name: str
    description: str
    source_data: List[SourceData]
    objectives_config: List[Tuple[StepConfig, StepConfig]]