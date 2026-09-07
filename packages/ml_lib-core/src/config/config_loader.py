import json

from .config_schema import SourceData
from .config_process import InputConfig, ProcessConfig, StepConfig
from .config_spliter import SplitConfig

class ConfigLoader:
    def get_split_config(config_path: str) -> SplitConfig:
        with open(config_path, 'r') as file:
            config_dict = json.load(file)["data_config"]

        try:

            split_dict = config_dict["splits"]
            split_data = SplitConfig(
                name = split_dict["name"],
                dev_split_fraction = split_dict["dev_split_fraction"],
                dev_subsplits = split_dict["dev_subsplits"],
                tst_subsplits = split_dict["tst_subsplits"],
            )

            return split_data

        except:
           print("Error loading split configuration from file:", config_path) 

    def get_source_config(config_path: str) -> SourceData:
        with open(config_path, 'r') as file:
            config_dict = json.load(file)["data_config"]

        try:
            source_dict = config_dict["source"]
            source_data = SourceData(
                path = source_dict["path"],
                name = source_dict["name"],
                description = source_dict["description"],
                data_types = source_dict["data_types"]
            )

            return source_data

        except:
           print("Error loading source configuration from file:", config_path)

    def get_input_config(config_path: str) -> InputConfig:
        with open(config_path, 'r') as file:
            config_dict = json.load(file)["data_config"]

        try:
            source_dict = config_dict["source"]
            source_data = SourceData(
                path = source_dict["path"],
                name = source_dict["name"],
                description = source_dict["description"],
                data_types = source_dict["data_types"]
            )

            input_config = InputConfig(
                name = config_dict["name"],
                source_data = source_data,
                labels = config_dict["labels"],
                features = config_dict["features"]
            )

            return input_config

        except:
            print("Error loading input configuration from file:", config_path)

    def get_split_process_config(config_path: str) -> ProcessConfig:
        input_config = ConfigLoader.get_input_config(config_path)
        split_config = ConfigLoader.get_split_config(config_path)

        process_config = ProcessConfig(
            name = "Initial Split Process",
            description = "Process to split the dataset into dev and test sets and smaller subsplits for each set.",
            source_data = [input_config.source_data],
            objectives_config = [
                (
                    StepConfig(
                        name = "Input Original Dataset",
                        process_config = input_config
                    ),
                    StepConfig(
                        name = "Split Original Dataset",
                        process_config = split_config,
                        discard_after = False
                    )
                )
            ]
        )

        return process_config