import requests
import pandas as pd
from .utils import BearerAuth, load_yaml
import os 

os.environ['MINDER_TOKEN'] = load_yaml('info.yaml')['token']
AUTH = BearerAuth(os.getenv('MINDER_TOKEN'))


def upload_file(file_2_upload):
    file = open(f"{file_2_upload}", "rb")
    binary_data = file.read()
    requests.put(f'https://research.minder.care/api/reports/{file_2_upload}',
                        data=binary_data,
                        headers={'content-type': 'text/html'},
                        auth=AUTH)
    r1 = requests.get('https://research.minder.care/api/reports', auth=auth)
    r1 = pd.Series(r1.json())
    return f'https://research.minder.care/{r1[r1.str.contains(file_2_upload)].values[0]}'