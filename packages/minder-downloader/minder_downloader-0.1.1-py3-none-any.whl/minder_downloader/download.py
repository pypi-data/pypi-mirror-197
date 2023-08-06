import requests
import json
import logging
import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm
import os
from pathlib import Path
from time import sleep
from io import StringIO
from typing import List
from .utils import BearerAuth, date2iso, load_yaml
from .info import _minder_datasets_info,_minder_organizations_info
from .update import get_token
# Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
#
ROOT =  Path(__file__).parent
INFO_PATH = f'{ROOT}{os.sep}info.yaml'
os.environ['MINDER_TOKEN'] = load_yaml(INFO_PATH)['token']
SERVER = load_yaml(INFO_PATH)['server']
HEADERS = load_yaml(INFO_PATH)['headers']
AUTH = BearerAuth(os.getenv('MINDER_TOKEN'))


class MinderDatasetDownload:
    """Class for downloading Minder research portal datasets."""

    def __init__(self, 
                 since: dt.datetime, 
                 until: dt.datetime, 
                 datasets: List[str],
                 organizations:list = None):
        self.since = date2iso(since)
        self.until = date2iso(until)
        self.datasets = datasets
        self.datasets_info = _minder_datasets_info()
        self.organizations_info = _minder_organizations_info()  
        self.headers = HEADERS
        self.server = SERVER + '/export'
        self.data_request = {
            'since': self.since,
            'until': self.until,
            'datasets': {
                ds: {"columns": self.datasets_info.query('datasets == @ds').availableColumns.iat[0]}
                for ds in self.datasets
            }
        }
        if organizations:
            self.data_request['organizations'] = organizations
        self._request_id = ''
        self._csv_url = pd.DataFrame()



    def post_request(self) -> None:
        """Sends a POST request to the Minder research portal and stores the resulting request ID."""
        request = requests.post(
            self.server,
            data=json.dumps(self.data_request),
            headers=self.headers,
            auth=BearerAuth(os.getenv('MINDER_TOKEN'))
        )
        self._request_id = request.headers['Content-Location'].split('/')[-1]
        logging.debug(f"request_id: {self._request_id}")

    def _get_output_urls(self) -> pd.DataFrame:
        """Retrieves the output URLs for a previously sent request ID."""
        with requests.get(f'{self.server}/{self._request_id}/', auth=AUTH) as request:
            request_elements = pd.DataFrame(request.json())
            output = pd.DataFrame()
            if request_elements.status.iat[0] == 202:
                logging.debug('*')
            elif request_elements.status.iat[0] == 200:
                if 'output' in request_elements.index:
                    output = pd.DataFrame(request_elements.loc['output'].jobRecord)
                    if output.empty:
                        logging.debug(f'{self._request_id} has no info')
                        output = pd.DataFrame([False])
                    else:
                        logging.debug(f'{self._request_id} received with info')
            else:
                logging.debug(f'Unexpected {request_elements.status.iat[0]} status')
        return output

    def process_request(self, sleep_time: int = 2) -> None:
        """Polls the Minder research portal for output URLs until they become available."""
        logging.debug(f'Processing {self.datasets}')
        while self._csv_url.empty:
            sleep(sleep_time)
            self._csv_url = self._get_output_urls()
   

    def _persistent_download(self, url: str, idx: int) -> pd.DataFrame:
        """Downloads and returns data from a given URL, retrying if necessary."""
        df = pd.DataFrame()
        while df.empty:
            try:
                with requests.get(url, stream=True, auth=AUTH) as request:
                    decoded_data = StringIO(request.content.decode('utf-8-sig'))
                    df = pd.read_csv(decoded_data, sep=',', engine='python')
                    df['source'] = self._csv_url.type[idx]
            except:
                logging.debug(self._request_id)
            sleep(2)
        return df

    def download_data(self) -> pd.DataFrame:
        """Downloads data from the Minder research portal and returns it as a Pandas DataFrame."""
        self.post_request()
        self.process_request()

        data = []
        if not self._csv_url.empty and 'url' in self._csv_url:
            for idx, url in enumerate(tqdm(self._csv_url.url,
                                           desc=f'Downloading {self.datasets}',
                                           dynamic_ncols=True)):
                df = self._persistent_download(url, idx)
                data.append(df)
            self.data = pd.concat(data).reset_index(drop=True)
            self.data = self.data[np.any(self.data.values == self.data.columns.values.reshape(1, -1), axis=1) == False]
            self.data = self.data.replace({'false': False, 'true': True})
        else:
            print('No data in this period')
            self.data = pd.DataFrame()
        return self.data
    

    
def load(since: dt.datetime, until: dt.datetime, datasets: list, organizations: list = None) -> pd.DataFrame:
    downloader = MinderDatasetDownload(since, until, datasets, organizations)
    downloader.post_request()
    downloader.process_request()
    data = downloader.download_data()
    return data    