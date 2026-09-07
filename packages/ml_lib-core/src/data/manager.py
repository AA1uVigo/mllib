import os

from ..config import ConfigLoader
from .structure import DatasetStructure
from ..processor import LinearProcessor

class DatasetManager:
    def __init__(self, config_path: str, output_dir: str):
        self.config_path = config_path
        self.source_config = ConfigLoader.get_source_config(config_path)
        self.split_config = ConfigLoader.get_split_config(config_path)
        self.dataset_structure = DatasetStructure(output_dir)
        self.dataset_structure.add_subsplits(self.split_config.dev_subsplits, self.split_config.tst_subsplits)
        self.create_dirs()

    def create_dirs(self):
        os.makedirs(self.dataset_structure.original_data, exist_ok=True)
        os.makedirs(self.dataset_structure.dev_split, exist_ok=True)
        os.makedirs(self.dataset_structure.tst_split, exist_ok=True)
        for subsplit_dir in self.dataset_structure.dev_subsplit_list.values():
            os.makedirs(subsplit_dir, exist_ok=True)
        for subsplit_dir in self.dataset_structure.tst_subsplit_list.values():
            os.makedirs(subsplit_dir, exist_ok=True)
        os.makedirs(self.dataset_structure.metadata, exist_ok=True)

    def link_dataset(self):
        file_name = os.path.basename(self.source_config.path)
        new_path = os.path.join(self.dataset_structure.original_data, file_name)
        if not os.path.exists(new_path):
            os.link(self.source_config.path, new_path)

    def create_dataset(self):
        process_config = ConfigLoader.get_split_process_config(self.config_path)
        split_processor = LinearProcessor(process_config, self.dataset_structure)
        split_processor.process()

    def get_dataset_name(self):
        return self.source_config.name

    def get_dataset_description(self):
        return self.source_config.description

    def get_dev_split_fraction(self):
        return self.split_config.dev_split_fraction
