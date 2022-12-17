import os
from os import environ as osenv
from os.path import abspath, dirname, join

# Global settings
BASE_DIR = dirname(dirname(abspath(__file__)))
osenv['BASE_DIR'] = BASE_DIR
osenv["PKG_DIR"] = join(BASE_DIR, "pkg")


# Print some var to verify if env is loaded
def verify():
    print('>>> Environment loading status <<<')
    print(f'--  Application base directory: {BASE_DIR}')
    print(f'--  Application name: {os.getenv("APP_NAME")}')
