import json

import click
from bripinfo.core import Output, Query, _current_dir, _remote_filename
from bripinfo.registro_br import setup_registrobr


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


@click.command(help='Query IP or CNPJ from Registro.br.')
@click.option('--type', '-t', help='Type of query: [ip, cnpj]')
@click.option('--search', '-s', help='Term to searched (ip or cnpj). Ex: 192.168.0.22 (ip) | 10942479000139 (cnpj)')
def query(type, search):
    qs = Query(Output().to_list())

    if type == 'ip':
        click.secho(json.dumps(qs.query_by_ip(search), indent=4, sort_keys=True), fg='green')
    elif type == 'cnpj':
        click.secho(json.dumps(qs.query_by_cnpj(search), indent=4, sort_keys=True), fg='green')
    else:
        click.echo('Choose one of the following valid types: [ip, cnpj]')


cli.add_command(setup)
cli.add_command(export)
cli.add_command(query)

cli()
