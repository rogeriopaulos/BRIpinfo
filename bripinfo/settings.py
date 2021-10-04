import logging
import os

# Configs (.ini)
# ------------------------------------------------------------------------------
CONFIG = {
    'registro_br': {
        'main_file': 'https://ftp.registro.br/pub/numeracao/origin/nicbr-asn-blk-latest.txt',
        'sha256_mainfile': 'https://ftp.registro.br/pub/numeracao/origin/nicbr-asn-blk-latest.txt.sha256'
    }
}

# General
# ------------------------------------------------------------------------------
ROOT_DIR = os.getcwd()
APP_DIR = f'{ROOT_DIR}/bripinfo'

# Logging
# ------------------------------------------------------------------------------
log_format = '[%(asctime)s][%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
LOGGER = logging.getLogger('root')
