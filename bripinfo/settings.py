import configparser
import logging
import os

# Configs (.ini)
# ------------------------------------------------------------------------------
CONFIG = configparser.ConfigParser()
CONFIG.read('bripinfo/config.ini')

# General
# ------------------------------------------------------------------------------
ROOT_DIR = os.getcwd()
APP_DIR = f'{ROOT_DIR}/bripinfo'

# Logging
# ------------------------------------------------------------------------------
log_format = '[%(asctime)s][%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
LOGGER = logging.getLogger('root')
