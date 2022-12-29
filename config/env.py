import os
from os import environ as osenv
from os.path import abspath, dirname

# Global settings
BASE_DIR = dirname(dirname(abspath(__file__)))
osenv['BASE_DIR'] = BASE_DIR


def verify():
    """Print some var to verify if env is loaded"""
    print('>>> Environment loading status <<<')
    print(f'--  Application base directory: {BASE_DIR}')
    print(f'--  Application name: {os.getenv("APP_NAME")}')
