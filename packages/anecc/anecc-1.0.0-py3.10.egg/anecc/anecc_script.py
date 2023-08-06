
import click
from anecc import anecc_compile

@click.command()
@click.option('--path', '-i', required=True, type=str)
@click.option('--name', '-n', type=str)
@click.option('--outd', '-o', type=str, default='')
def cli(path, name, outd):
	anecc_compile(path, name, outd)
