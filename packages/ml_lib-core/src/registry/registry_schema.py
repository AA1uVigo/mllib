from typing import List, Dict, Iterator, TypeVar, Generic, Callable

from ..config import BaseConfig
from ..data import DatasetStructure
ElementType = TypeVar("ElementType")

class Registry(Generic[ElementType]):
    def __init__(self, family_name: str) -> None:
        self.family_name = family_name
        self._items: Dict[str, type[ElementType]] = {}

    def register(self, override: bool = False) -> Callable[[type[ElementType]], type[ElementType]]:
        def deco(cls: type[ElementType]) -> type[ElementType]:
            key = getattr(cls, "name", "")
            if not key:
                pass
            if key in self and not override:
                pass
            self._items[key] = cls
            return cls
        return deco

    def create(self, config: BaseConfig, dataset_structure: DatasetStructure) -> ElementType:
        if config.name not in self:
            pass
        return self._items[config.name](config, dataset_structure)

    def names(self) -> List[str]:
        return sorted(self._items)

    def __contains__(self, name: str) -> bool:
        return name in self._items

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)

class InstanceGenerator:
    registries: Dict[str, Registry] = {}

    def add_registry(self, registry: Registry) -> None:
        self.registries[registry.family_name] = registry

    def create_instance(self, config: BaseConfig, dataset_structure: DatasetStructure) -> ElementType:
        if config.family_name not in self.registries:
            pass
        registry = self.registries[config.family_name]
        return registry.create(config, dataset_structure)
