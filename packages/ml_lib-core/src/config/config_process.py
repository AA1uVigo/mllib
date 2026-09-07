
from dataclasses import dataclass
from typing import Tuple, List, ClassVar

from ..config import BaseConfig, SourceData


@dataclass
class InputConfig(BaseConfig):
    source_data: SourceData
    labels: List[str]
    features: List[str]
    family_name: ClassVar[str] = "input_config"

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