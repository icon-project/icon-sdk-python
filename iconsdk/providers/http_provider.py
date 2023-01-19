# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
from json.decoder import JSONDecodeError
from time import time
from typing import Union
from urllib.parse import urlparse

import requests
from multimethod import multimethod

from iconsdk.exception import JSONRPCException, URLException
from iconsdk.providers.provider import Provider
from iconsdk.utils import to_dict


class HTTPProvider(Provider):
    """
    The HTTPProvider takes the full URI where the server can be found.
    For local development this would be something like 'http://localhost:9000'.
    """

    @multimethod
    def __init__(self, base_domain_url: str, version: int, request_kwargs: dict = None):
        """
        The initializer to be set with base domain URL and version.

        :param base_domain_url: base domain URL as like <scheme>://<host>:<port>
        :param version: version for RPC server
        :param request_kwargs: kwargs for setting to head of request
        """
        uri = urlparse(base_domain_url)
        if uri.path != '':
            raise URLException('Path is not allowed')
        self._serverUri = f'{uri.scheme}://{uri.netloc}'
        self._channel = ''
        self._version = version
        self._request_kwargs = request_kwargs or {}
        self._generate_url_map()

    @multimethod
    def __init__(self, full_path_url: str, request_kwargs: dict = None):
        """
        The initializer to be set with full path url as like <scheme>://<host>:<port>/api/v3.
        If you need to use a channel, you can use it such as <scheme>://<host>:<port>/api/v3/{channel}.

        :param full_path_url: full path URL as like <scheme>://<host>:<port>/api/v3
        :param request_kwargs: kwargs for setting to head of request
        """
        uri = urlparse(full_path_url)
        self._serverUri = f'{uri.scheme}://{uri.netloc}'
        self._channel = self._get_channel(uri.path)
        self._version = 3
        self._request_kwargs = request_kwargs or {}
        self._generate_url_map()

    def _generate_url_map(self):
        def _add_channel_path(url: str):
            if self._channel:
                return f"{url}/{self._channel}"
            return url

        self._URL_MAP = {
            'icx': _add_channel_path(f"{self._serverUri}/api/v{self._version}"),
            'btp': _add_channel_path(f"{self._serverUri}/api/v{self._version}"),
            'debug': _add_channel_path(f"{self._serverUri}/api/v{self._version}d"),
        }

    @staticmethod
    def _get_channel(path: str):
        tokens = re.split("/(?=[^/]+$)", path.rstrip('/'))
        if tokens[0] == '/api/v3':
            return tokens[1]
        elif tokens == ['/api', 'v3']:
            return ''
        raise URLException('Invalid URI path')

    def __str__(self):
        return "RPC connection to {0}".format(self._serverUri)

    @to_dict
    def _get_request_kwargs(self) -> dict:
        if 'headers' not in self._request_kwargs:
            yield 'headers', {'Content-Type': 'application/json'}
        for key, value in self._request_kwargs.items():
            yield key, value

    @staticmethod
    def _make_post_request(request_url: str, data: dict, **kwargs) -> requests.Response:
        kwargs.setdefault('timeout', 10)
        with requests.Session() as session:
            response = session.post(url=request_url, data=json.dumps(data), **kwargs)
        return response

    def _make_id(self) -> int:
        return int(time())

    def make_request(self, method: str, params=None, full_response: bool = False) -> Union[str, list, dict]:
        rpc_dict = {
            'jsonrpc': '2.0',
            'method': method,
            'id': self._make_id()
        }
        if params:
            rpc_dict['params'] = params

        req_key = method.split('_')[0]
        request_url = self._URL_MAP.get(req_key)
        response = self._make_post_request(request_url, rpc_dict, **self._get_request_kwargs())
        try:
            return self._return_custom_response(response, full_response)
        except JSONDecodeError:
            raw_response = response.content.decode()
            raise JSONRPCException(f'Unknown response: {raw_response}')

    @staticmethod
    def _return_custom_response(response: requests.Response, full_response: bool = False) -> Union[str, list, dict]:
        content = json.loads(response.content)
        if full_response:
            return content
        if response.ok:
            return content['result']
        raise JSONRPCException(content["error"])
