# -*- coding: utf-8 -*-
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
import requests
from logging import getLogger
from itertools import count
from iconsdk.utils import to_dict
from iconsdk.providers.provider import Provider
from iconsdk.utils import set_logger
from iconsdk.exception import JSONRPCException


class HTTPProvider(Provider):
    """
    The HTTPProvider takes the full URI where the server can be found.
    For local development this would be something like http://localhost:9000.
    """

    endpoint_uri = None
    _request_kwargs = None

    logger = getLogger("HTTPProvider")

    # No need to use logging, remove the line.
    set_logger(logger, 'DEBUG')

    def __init__(self, endpoint_uri=None, request_kwargs=None):
        self.logger.debug("Init HTTP Provider")
        self.request_counter = count()
        if endpoint_uri is None:
            raise JSONRPCException("Not found endpoint uri.")
        else:
            self.endpoint_uri = endpoint_uri
        self._request_kwargs = request_kwargs or {}

    def __str__(self):
        return "RPC connection {0}".format(self.endpoint_uri)

    @to_dict
    def get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield 'headers', {'Content-Type': 'application/json'}
        for key, value in self._request_kwargs.items():
            yield key, value

    @staticmethod
    def make_post_request(endpoint_uri, data, **kwargs):
        kwargs.setdefault('timeout', 10)
        with requests.Session() as session:
            response = session.post(url=endpoint_uri, data=json.dumps(data), **kwargs)
        return json.loads(response.content)

    def make_request(self, method, params=None):
        rpc_dict = {
            'jsonrpc': '2.0',
            'method': method,
            'id': 1234
        }

        if params:
            rpc_dict['params'] = params

        self.logger.debug("request HTTP\nURI: %s\nMethod: %s\nData: %s",
                              self.endpoint_uri, method, rpc_dict)

        response = self.make_post_request(self.endpoint_uri, rpc_dict, **self.get_request_kwargs())
        self.logger.debug("response HTTP\nResponse:%s", response)
        return self.return_customed_response(response)

    @staticmethod
    def return_customed_response(response):
        try:
            return response["result"]
        except KeyError:
            raise JSONRPCException(response["error"])

    def is_connected(self):
        try:
            self.logger.debug("Connected")
            response = self.make_request('icx_getLastBlock', [])
        except IOError:
            return False
        else:
            return True

