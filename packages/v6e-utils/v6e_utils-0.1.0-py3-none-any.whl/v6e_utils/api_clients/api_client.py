#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#
from typing import Dict
from urllib.parse import urljoin

# import jwt as jwt
import requests
import logging

LOGGER = logging.getLogger(__name__)


class V6eApiClient:
    base_url: str = None
    params: Dict = {}
    headers: Dict = {}
    api_url: str = None
    access_token = None

    def __init__(self, base_url, headers=None, endpoint_root=None, token=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.endpoint_root = endpoint_root or None
        self.access_token = token or None
        if self.endpoint_root is not None:
            self.api_url = urljoin(self.base_url, self.endpoint_root) + '/'
        else:
            self.api_url = urljoin(self.base_url) + '/'

    def get(self, endpoint, params=None):
        url = urljoin(self.api_url, endpoint) + "/"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def test_connection(self):
        response = requests.head(self.base_url, headers=self.headers)
        response.raise_for_status()
        return True

    def _build_headers(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json'
        }
        return headers

    # def extract_token_parameters(self):
    #     token_parts = self.access_token.split('.')
    #     token_header = jwt.get_unverified_header(self.access_token)
    #     token_claims = jwt.decode(self.access_token, options={"verify_signature": False})
    #     return token_header, token_claims
