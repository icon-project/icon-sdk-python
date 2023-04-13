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
from time import time, monotonic
from typing import Union, Optional
from urllib.parse import urlparse, urlunparse

import requests
from multimethod import multimethod
from websocket import WebSocket, WebSocketTimeoutException

from iconsdk.exception import JSONRPCException, URLException
from iconsdk.providers.provider import Provider, MonitorSpec, Monitor, MonitorTimeoutException
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

        def _make_ws_url(url: str, name: str) -> str:
            url = urlparse(url)
            if url.scheme == 'http':
                scheme = 'ws'
            elif url.scheme == 'https':
                scheme = 'wss'
            else:
                raise URLException('unknown scheme')
            return urlunparse((scheme, url.netloc, f'{url.path}/{name}', '', '', ''))

        if self._channel:
            self._WS_MAP = {
                'block': _make_ws_url(self._URL_MAP['icx'], 'block'),
                'event': _make_ws_url(self._URL_MAP['icx'], 'event'),
                'btp': _make_ws_url(self._URL_MAP['btp'], 'btp'),
            }
        else:
            self._WS_MAP = None

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

    def make_monitor(self, spec: MonitorSpec, keep_alive: Optional[float] = None) -> Monitor:
        if self._WS_MAP is None:
            raise Exception(f'Channel must be set for socket')
        path = spec.get_path()
        params = spec.get_request()
        if path not in self._WS_MAP:
            raise Exception(f'No available socket for {path}')
        return WebSocketMonitor(self._WS_MAP[path], params, keep_alive=keep_alive)


class WebSocketMonitor(Monitor):
    def __init__(self, url: str, params: dict, keep_alive: Optional[float] = None):
        self.__client = WebSocket()
        self.__keep_alive = keep_alive or 30
        self.__client.connect(url)
        self.__client.send(json.dumps(params))
        result = self.__read_json(None)
        if 'code' not in result:
            raise Exception(f'invalid response={json.dumps(result)}')
        if result['code'] != 0:
            raise Exception(f'fail to monitor err={result["message"]}')

    def close(self):
        self.__client.close()

    def __read_json(self, timeout: Optional[float] = None) -> any:
        now = monotonic()
        limit = None
        if timeout is not None:
            limit = now + timeout

        while True:
            try:
                if limit is not None:
                    self.__client.timeout = min(limit - now, self.__keep_alive)
                else:
                    self.__client.timeout = self.__keep_alive
                return json.loads(self.__client.recv())
            except WebSocketTimeoutException as e:
                now = monotonic()
                if limit is None or now < limit:
                    self.__client.send(json.dumps({"keepalive": "0x1"}))
                    continue
                else:
                    raise MonitorTimeoutException()

    def read(self, timeout: Optional[float] = None) -> any:
        return self.__read_json(timeout=timeout)
