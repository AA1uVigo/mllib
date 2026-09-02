import json

from .config_schema import SourceData, SplitConfig

class ConfigLoader:
    def get_splt_config(config_path: str) -> SplitConfig:
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

            split_dict = config_dict["splits"]
            split_data = SplitConfig(
                source_data = source_data,
                dev_split_fraction = split_dict["dev_split_fraction"],
                dev_subsplits = split_dict["dev_subsplits"],
                tst_subsplits = split_dict["tst_subsplits"],
            )

            return split_data

        except:
            pass