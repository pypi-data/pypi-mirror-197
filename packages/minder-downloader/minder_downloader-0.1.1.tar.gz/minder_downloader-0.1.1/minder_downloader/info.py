import requests
import pandas as pd
from .utils import BearerAuth, load_yaml
import os 
from pathlib import Path

# Load credentials and server information from YAML file
ROOT =  Path(__file__).parent
INFO_PATH = f'{ROOT}{os.sep}info.yaml'
os.environ['MINDER_TOKEN'] = load_yaml(INFO_PATH)['token']
SERVER = load_yaml(INFO_PATH)['server']
HEADERS = load_yaml(INFO_PATH)['headers']
AUTH = BearerAuth(os.getenv('MINDER_TOKEN'))




def _minder_datasets_info() -> pd.DataFrame:
    """Returns minder research portal datasets."""
    info_path = SERVER + '/info/datasets'
    request = requests.get(info_path, auth=AUTH)
    domains = request.json()['Categories'].keys()
    info = pd.concat([
        pd.DataFrame(request.json()['Categories'][domain])
        .T.assign(domain=domain)
        for domain in domains
    ])
    info.index = info.index.rename('datasets')
    info = info.reset_index()
    return info


def _minder_organizations_info() -> pd.DataFrame:
    """Returns minder research portal organizations."""
    info_path = SERVER + '/info/organizations'
    request = requests.get(info_path, auth=AUTH)
    info = pd.DataFrame(request.json()['organizations'])
    return info