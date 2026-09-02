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
    split_config = ConfigLoader.get_splt_config(config_file)

    click.echo(f"Dataset: {split_config.source_data.name}")
    click.echo(f"Description: {split_config.source_data.description}")
    click.echo(f"Developer set fraction: {split_config.dev_split_fraction}")
    click.echo(f"Test set fraction: {split_config.tst_split_fraction}")

    dataset_structure = DatasetStructure(output_dir)
    dataset_structure.add_subsplits(split_config)
