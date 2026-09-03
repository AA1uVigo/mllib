from abc import ABC, abstractmethod
import multiprocessing as mp
import pandas as pd

from ..data import DatasetStructure
from ..config import BaseConfig, InputConfig, ProcessConfig

class ElementalProcessor(ABC):
    def __init__(self, config: BaseConfig, dataset_structure: DatasetStructure):
        self.config = config
        self.dataset_structure = dataset_structure

    @abstractmethod
    def step(self):
        raise NotImplementedError("Subclasses must implement the process method.")

class Processor(ABC):
    def __init__(self, process_config: ProcessConfig, dataset_structure: DatasetStructure):
        self.process_config = process_config
        self.dataset_structure = dataset_structure
        self.started = False

    @abstractmethod
    def _subprocess(self):
        raise NotImplementedError("Subclasses must implement the subprocess method for mutithread processing.")

    @classmethod
    def _worker(cls, payload: dict):
        instance = payload["instance"]
        args     = payload["args"]
        kwargs   = payload["kwargs"]
        return instance._subprocess(*args, **kwargs)

    @abstractmethod
    def _lazy_execute(self):
        raise NotImplementedError("Subclasses must implement the process method.")

    @abstractmethod
    def process(self, multithread=False, num_workers=mp.cpu_count, lazy=True):
        raise NotImplementedError("Subclasses must implement the process method.")

class LinearProcessor(Processor):
    def __init__(self, process_config: ProcessConfig, dataset_structure: DatasetStructure):
        super().__init__(process_config, dataset_structure)

    def _lazy_execute(self):
        aux = self.data.copy()
        for step in self.linear_process:
            aux = step.step(aux)

        return aux

    def process(self, lazy=True):
        if lazy and not self.started:
            return self._lazy_execute()

        process_config = self.process_config.objectives_config

        for i, step_config in enumerate(process_config):
            if step_config[0].process_config.isinstance(InputConfig):
                input_file = step_config[0].process_config.source_data.path
                output_config = step_config[1]
                self.linear_process = [output_config.process_config.types.create(output_config.process_config.name)]

                with open(input_file, 'r') as file:
                    self.data = pd.read_csv(file)

                output = self.linear_process[-1].step(self.data)
                process_config.pop(i)
                
                break
        while process_config:
            for i, step_config in enumerate(process_config):
                input_config = step_config[0]
                new_output_config = step_config[1]

                if input_config.name == new_output_config.name:
                    self.linear_process.append(new_output_config.process_config.types.create(new_output_config.process_config.name))
                    output = self.linear_process[-1].step(output)
                    process_config.pop(i)
                    break

        if lazy:
            self.started = True