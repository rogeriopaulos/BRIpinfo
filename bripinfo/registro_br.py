import datetime as dt
import json

from bripinfo import settings
from bripinfo.core import BaseData


class RegistroBrMetadata(BaseData):
    """
    self.data -> {
        'source': <str>,
        'timestamp': <str>,
        'sha256': <str>,
    }
    """

    url = settings.CONFIG['registro.br']['sha256_mainfile']
    content_name = 'metadados'
    source = 'Registro.br'

    def __init__(self):
        super().__init__()
        self.equal_sha256 = self._is_equal_sha256()

    def _is_equal_sha256(self):
        try:
            with open(self._full_filepath, 'r') as f:
                data = json.load(f)

            local_sha256 = data['sha256'].strip()
            remote_sha256 = self._raw_content.splitlines()[0].split('=')[-1].strip()

            result = True if local_sha256 == remote_sha256 else False
        except FileNotFoundError:
            result = False

        return result

    def _can_save(self):
        return True if not self.equal_sha256 else False

    def _data(self) -> dict:
        sha256 = self._raw_content.splitlines()[0].split('=')[-1].strip()

        data = {
            'source': self.url,
            'timestamp': dt.datetime.now().strftime('%Y-%d-%mT%H:%M:%S'),
            'sha256': sha256
        }

        return data


class RegistroBrData(BaseData):
    """
    self.data -> [{
        'ref': <str>,
        'name': <str>,
        'cnpj': <str>,
        'ips': <list>
    }, (...)]
    """

    url = settings.CONFIG['registro.br']['main_file']
    content_name = 'conteúdo'
    source = 'Registro.br'

    def _data(self) -> dict:
        content = self._raw_content

        settings.LOGGER.info('Estruturando o conteúdo do Registro.br')
        content = [line.split('|') for line in content.splitlines()]
        dataset = [
            {
                'ref': line[0],
                'name': line[1],
                'cnpj': line[2],
                'ips': list(line[3:])
            }
            for line in content]

        return dataset

    def _can_save(self):
        return True


def setup_registrobr():
    metadata = RegistroBrMetadata()
    is_equal_sha256 = metadata.equal_sha256
    if not is_equal_sha256:
        metadata.create_or_update()

        main_content = RegistroBrData()
        main_content.create_or_update()
    else:
        settings.LOGGER.info('Os dados do Registro.br encontram-se atualizados.')

    settings.LOGGER.info('Configuração finalizada!')
