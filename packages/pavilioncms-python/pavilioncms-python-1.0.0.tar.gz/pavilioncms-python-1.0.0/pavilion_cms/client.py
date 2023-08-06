"""Main module."""

import requests

from pavilion_cms.utils import handle_errors
from pavilion_cms.__version__ import __version__


BASE_URL = "https://api.v1.pavilioncms.com/"


class Client(object):
    def __init__(self, read_token: str, base_url: str = None):
        self._session = requests.Session()
        self._session.headers.update({"ReadToken": read_token})
        self._session.headers.update({"Content-Type": "application/json"})
        self._session.headers.update({"Accept": "application/json"})
        self._session.headers.update({"User-Agent": "pavilioncms-python-client"})
        self._session.headers.update({"X-Pavilion-Client": f"Python/{__version__}"})

        if not base_url:
            self._base_url = BASE_URL
        else:
            self._base_url = base_url

        self.tag_url = f"{self._base_url}/tag"
        self.category_url = f"{self._base_url}/category"
        self.post_url = f"{self._base_url}/post"
        self.user_url = f"{self._base_url}/user"

    def _make_list_request(self, url_path, params=None):
        response = self._session.get(url_path, params=params)
        handle_errors(response)
        return response.json()

    def _make_single_request(self, url_path) -> dict:
        response = self._session.get(url_path)
        handle_errors(response)
        return response.json()
