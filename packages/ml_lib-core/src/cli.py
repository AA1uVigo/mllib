import click
import json

from .data import DatasetManager

@click.group()
def cli():
    pass

@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def dataset_create(config_file, output_dir):
    click.echo(f"Loading configuration from: {config_file}")
    manager = DatasetManager(config_file, output_dir)

    click.echo(f"Dataset: {manager.get_dataset_name()}")
    click.echo(f"Description: {manager.get_dataset_description()}")
    click.echo(f"Developer set fraction: {manager.get_dev_split_fraction()}")

    manager.link_dataset()
    manager.create_dataset()
