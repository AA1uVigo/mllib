from dataclasses import dataclass
from typing import Dict

@dataclass
class SourceData:
    path: str
    name: str
    description: str
    data_types: Dict[str, str]

@dataclass
class BaseConfig:
    name: str
    family_name: str
