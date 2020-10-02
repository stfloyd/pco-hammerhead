import os
import sys
import logging


# -----------------------------------------------------------------------------
# Application Information

PROGRAM_NAME = 'pcotagger'
PROGRAM_NAME_VERBOSE = 'PCO Group Type Tagger'
PROGRAM_DESCRIPTION = 'A handy script to apply a tag group to an entire group type in Planning Center Online.'
PROGRAM_VERSION = '0.1'

CLI_HELP_TEXT = \
f"""
{PROGRAM_NAME_VERBOSE}
{PROGRAM_DESCRIPTION}

  _____   _____ ____    _______       _____  _____ 
 |  __ \ / ____/ __ \  |__   __|/\   / ____|/ ____|
 | |__) | |   | |  | |    | |  /  \ | |  __| (___  
 |  ___/| |   | |  | |    | | / /\ \| | |_ |\___ \ 
 | |    | |___| |__| |    | |/ ____ \ |__| |____) |
 |_|     \_____\____/     |_/_/    \_\_____|_____/ 
"""


# -----------------------------------------------------------------------------
# Application Paths

BASE_DIR = os.getcwd()

LOGS_DIR = os.path.join(BASE_DIR, 'logs/')
DEFAULT_LOG_FILE = os.path.join(LOGS_DIR, f'{PROGRAM_NAME}.log')
DEBUG_LOG_FILE = os.path.join(LOGS_DIR, f'{PROGRAM_NAME}.debug.log')
ERROR_LOG_FILE = os.path.join(LOGS_DIR, f'{PROGRAM_NAME}.error.log')

CONFIG_DIR = os.path.join(BASE_DIR, 'config/')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')


# -----------------------------------------------------------------------------
# Application Settings & Configuration

DEBUG = False

# format:
# 0         1 
# level     filepath
FILE_LOGGERS = [
    (logging.INFO, DEFAULT_LOG_FILE),
    (logging.DEBUG, DEBUG_LOG_FILE),
    (logging.ERROR, ERROR_LOG_FILE)
]

# format:
# 0         1 
# level     stream
STREAM_LOGGERS = [
    (logging.INFO, sys.stdout)
]


# General logging settings/customization
LOG_BACKUP_COUNT = 10
LOG_FILE_MAX_KB = 5000
LOG_FMT = '%(asctime)-8s %(name)-16s %(levelname)-8s %(message)s'
LOG_TIME_FMT = '%Y-%m-%d %H:%M:%S'


# 12-hour: %I:%M %p
# 24-hour: %H:%M
TIME_FMT = '%I:%M %p'
TIMEZONE = 'America/New_York'


DEFAULT_CONFIG = {
    'value_a': 10
}


def list_configs():
    config_files = [f for f in os.listdir(CONFIG_DIR) if os.path.isfile(os.path.join(CONFIG_DIR, f)) and f[-13:] != '.example.json']
    return config_files
