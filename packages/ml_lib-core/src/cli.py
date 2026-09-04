import click
import json

from .config import ConfigLoader
from .data import DatasetStructure

@click.group()
def cli():
    pass

@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def dataset_create(config_file, output_dir):
    click.echo(f"Loading configuration from: {config_file}")
    process_config = ConfigLoader.get_split_process_config(config_file)
    split_config = ConfigLoader.get_split_config(config_file)

    click.echo(f"Dataset: {process_config.source_data[0].name}")
    click.echo(f"Description: {process_config.source_data[0].description}")
    click.echo(f"Developer set fraction: {split_config.dev_split_fraction}")
    click.echo(f"Test set fraction: {split_config.tst_split_fraction}")

    dataset_structure = DatasetStructure(output_dir)
    dataset_structure.add_subsplits(split_config)

    split_processor = process_config.types.create(process_config.name, process_config, dataset_structure)
    split_processor.process(multithread=False, lazy=False)
