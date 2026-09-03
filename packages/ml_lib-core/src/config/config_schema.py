from dataclasses import dataclass
from types import Tuple, List, Dict, Optional
from ..registry import Registry

@dataclass
class SourceData:
    path: str
    name: str
    description: str
    data_types: Dict[str, str]

@dataclass
class BaseConfig:
    name: str
    types: Optional[Registry[BaseConfig]]

@dataclass
class InputConfig(BaseConfig):
    source_data: SourceData
    labels: List[str]
    features: List[str]

@dataclass
class StepConfig:
    name: str
    process_config: BaseConfig
    discard_after: bool = True

@dataclass
class ProcessConfig:
    name: str
    description: str
    source_data: List[SourceData]
    objectives_config: List[Tuple[StepConfig, StepConfig]]