import csv
import json
import os
from abc import ABCMeta, abstractmethod

import requests
from requests.exceptions import ConnectionError

from bripinfo import settings


class BaseData(metaclass=ABCMeta):

    def __init__(self):
        self._raw_content = self._get_remote_content()

    @property
    def _full_filepath(self):
        output_filename = self._get_remote_filename()
        return f'{settings.APP_DIR}/_files/{output_filename}.json'

    def _get_remote_filename(self):
        return self.url.split('/')[-1]

    def _get_remote_content(self):
        try:
            settings.LOGGER.info(f'Obtendo {self.content_name} do Registro.br (ftp)')
            response = requests.get(self.url)
            return response.text
        except ConnectionError:
            settings.LOGGER.error('Não foi possível obter os dados do Registro.br (ftp)')

    def create_or_update(self):
        if not os.path.exists(self._full_filepath) or self._can_save():
            self._write_file()

    @abstractmethod
    def _can_save(self) -> bool:
        ...

    def _write_file(self):
        data = self._data()
        settings.LOGGER.info(f'Salvando arquivo de {self.content_name} do Registro.br')
        with open(self._full_filepath, 'w', encoding='latin1') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

    @abstractmethod
    def _data(self) -> dict:
        ...


class Output:

    _remote_filename = settings.CONFIG['registro.br']['main_file'].split('/')[-1]

    def __init__(self):
        self._raw_data = self._get_main_content()

    def _get_main_content(self):
        with open(self._get_filepath(), 'r') as f:
            data = json.load(f)
        return data

    def _get_filepath(self):
        filedir = f'{settings.APP_DIR}/_files'
        return f'{filedir}/{self._remote_filename}.json'

    def to_list(self):
        """
        Return a list of dicts
        """
        return self._raw_data

    def to_json(self, filename=None, destination=os.getcwd()):
        try:
            fullpath = self._get_fullpath_by_ext(filename, destination, 'json')
            with open(fullpath, 'w', encoding='utf-8') as outfile:
                json.dump(self._raw_data, outfile, ensure_ascii=False)
        except IOError:
            settings.LOGGER.error('I/O error')

    def to_csv(self, filename=None, destination=os.getcwd()):
        fullpath = self._get_fullpath_by_ext(filename, destination, 'csv')
        csv_columns = list(self._raw_data[0].keys())

        try:
            with open(fullpath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self._raw_data:
                    writer.writerow(data)
        except IOError:
            settings.LOGGER.error('I/O error')

    def _get_fullpath_by_ext(self, name, destination, ext):
        filename = name if name else self._remote_filename
        if filename == self._remote_filename:
            filename = filename.split('.')[0]

        return f'{destination}/{filename}.{ext}'
