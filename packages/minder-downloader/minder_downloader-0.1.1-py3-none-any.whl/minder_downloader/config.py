from .utils import path_exists, write_yaml,load_yaml
from .update import get_token
from pathlib import Path
import os


def check_config():
    root = Path(__file__).parent
    info_path = f'{root}{os.sep}info.yaml'
    if not path_exists(info_path):
        tmp = {'headers':{ 'Accept': 'text/plain',
                        'Connection': 'keep-alive',
                        'Content-type': 'application/json'},  
                'server': 'https://research.minder.care/api'}
        TOKEN = None
    else:
        tmp = load_yaml(info_path)
        TOKEN = tmp['token']
    if  TOKEN is None: 
        TOKEN = get_token()
    tmp['token'] = TOKEN
    write_yaml(info_path,tmp)
    

    

