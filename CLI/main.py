# super_cli/my_cli.py
import click
from CLI.commands import _foam_fluent_2D

@click.command()
def foam_fluent_2D():
    _foam_fluent_2D()

if __name__ == '__main__':
    super()
