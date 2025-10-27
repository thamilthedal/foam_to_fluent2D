# super_cli/my_cli.py
import click
from CLI.commands import _foam_fluent_2D

dir = click.option("--dir", prompt="Working directory", help="Enter folder path")

@click.command()
@dir
def foam_fluent_2D(dir):
    _foam_fluent_2D(dir)

if __name__ == '__main__':
    super()
