import os

import click
import settings
from core import Output
from registro_br import setup_registrobr

_current_dir = os.getcwd()
_remote_file = settings.CONFIG['registro.br']['main_file'].split('/')[-1]
_remote_filename = _remote_file.split('.')[0]


@click.group()
def cli():
    ...


@click.command(help='Load data from registro.br.')
def setup():
    setup_registrobr()


@click.command(help='Export data from registro.br to json/csv.')
@click.option('--format', '-f', default='json', help='Format: [json, csv]. Default: json.')
@click.option('--destination', '-d', default=_current_dir, help=f'Where to save. Default: "{_current_dir}".')
@click.option('--name', '-n', default=_remote_filename, help=f'Filename. Default: "{_remote_filename}"')
def export(format, destination, name):
    o = Output(filename=name, destination=destination)

    if format == 'csv':
        o.to_csv()
    elif format == 'json':
        o.to_json()
    else:
        click.echo('Choose one of the following formats: [json, csv]')


cli.add_command(setup)
cli.add_command(export)

cli()
