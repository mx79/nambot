from os import environ as osenv
from os.path import abspath, dirname, join
from dotenv import load_dotenv, find_dotenv

# ======== GLOBAL SETTINGS ======== #

BASE_DIR = dirname(dirname(abspath(__file__)))
osenv['BASE_DIR'] = BASE_DIR
osenv["PKG_DIR"] = join(BASE_DIR, "pkg")

# ======== LOAD ENVIRONMENT VARS (from .env) ======== #

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# ======== PRINT SOME VAR TO VERIFY IF ENV IS LOADED ======== #

def verify():
    print(f'>>> Environment loading status <<<')
    print(f'--  Application base directory: {BASE_DIR}')
    print(f'--  Dotenv file: {ENV_FILE}')
