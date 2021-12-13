import csv
import ipaddress
import json
import os
import re
from abc import ABCMeta, abstractmethod

import requests
from requests.exceptions import ConnectionError

from bripinfo import settings

_current_dir = os.getcwd()
_remote_file = settings.CONFIG['registro_br']['main_file'].split('/')[-1]
_remote_filename = _remote_file.split('.')[0]


class BaseData(metaclass=ABCMeta):

    def __init__(self):
        self._raw_content = self._get_remote_content()

    @property
    def _full_filepath(self):
        output_filename = self._get_remote_filename()
        return f'{settings.APP_DIR}/.files/{output_filename}.json'

    def _get_remote_filename(self):
        return self.url.split('/')[-1]

    def _get_remote_content(self):
        try:
            settings.LOGGER.info(f'Obtendo {self.content_name} do {self.source}')
            response = requests.get(self.url)
            return response.text
        except ConnectionError:
            settings.LOGGER.error(f'Não foi possível obter os dados do {self.source}')

    def create_or_update(self):
        if not os.path.exists(self._full_filepath) or self._can_save():
            self._write_file()

    @abstractmethod
    def _can_save(self) -> bool:
        ...

    def _write_file(self):
        data = self._data()
        settings.LOGGER.info(f'Salvando arquivo de {self.content_name} do {self.source}')
        with open(self._full_filepath, 'w', encoding='latin1') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

    @abstractmethod
    def _data(self) -> dict:
        ...


class Output:

    def __init__(self, filename=_remote_filename, destination=_current_dir):
        self.filename = filename
        self.destination = destination

        self._raw_data = self._get_main_content()

    def _get_main_content(self):
        try:
            with open(self._get_filepath(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            settings.LOGGER.error('Por favor, carregue os dados antes...')

    def _get_filepath(self):
        filedir = f'{settings.APP_DIR}/.files'
        remote_filename = settings.CONFIG['registro_br']['main_file'].split('/')[-1]
        return f'{filedir}/{remote_filename}.json'

    def to_list(self):
        """
        Return a list of dicts
        """
        return self._raw_data

    def to_json(self):
        try:
            fullpath = f'{self.destination}/{self.filename}.json'
            with open(fullpath, 'w', encoding='utf-8') as outfile:
                json.dump(self._raw_data, outfile, ensure_ascii=False)
                settings.LOGGER.info(f'Arquivo salvo: {fullpath}')
        except IOError:
            settings.LOGGER.error('I/O error')

    def to_csv(self):
        fullpath = f'{self.destination}/{self.filename}.csv'
        csv_columns = list(self._raw_data[0].keys())

        try:
            with open(fullpath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self._raw_data:
                    writer.writerow(data)
                settings.LOGGER.info(f'Arquivo salvo: {fullpath}')
        except IOError:
            settings.LOGGER.error('I/O error')


class Query:

    def __init__(self, listdata: list):
        self.listdata = listdata

    def query_by_ip(self, term: str) -> dict:
        try:
            return next(isp for isp in self.listdata for ip in isp['ips']
                        if ipaddress.ip_address(term) in ipaddress.ip_network(ip))
        except ValueError:
            settings.LOGGER.error('Esse endereço de IP não é válido.')

    def query_by_cnpj(self, term: str) -> dict:
        try:
            return next(isp for isp in self.listdata if re.sub("[^0-9]", "", isp.get('cnpj')).startswith(term))
        except StopIteration:
            settings.LOGGER.error(
                'Esse CNPJ não é válido. Informe apenas os números ou garanta que o CNPJ seja de uma ISP.'
            )
