# -*- coding: utf-8 -*-
# Copyright 2017-2018 ICON Foundation
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

import logging
import itertools
import requests
import json
from IconService.utils import to_dict
from IconService.providers.provider import Provider


def get_default_endpoint():
    return "https://testwallet.icon.foundation/api/v2"


class HTTPProvider(Provider):

    endpoint_uri = None
    _request_kwargs = None
    logger = logging.getLogger("IconService.providers.HTTPProvider")

    def __init__(self, endpoint_uri=None, request_kwargs=None):
        self.request_counter = itertools.count()
        if endpoint_uri is None:
            self.endpoint_uri = get_default_endpoint()
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
            response = session.post(url=endpoint_uri, json=data, **kwargs)
            response.raise_for_status()
        return json.loads(response.content)

    def make_request(self, method, params):
        self.logger.debug("Make request HTTP. URI is %s, Method is %s",
                          self.endpoint_uri, method)
        rpc_dict = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1234
        }

        if params:
            rpc_dict['params'] = params

        response = self.make_post_request(self.endpoint_uri, rpc_dict, **self.get_request_kwargs())
        self.logger.debug("Get response HTTP. URI is %s, "
                          "Method is %s, Response is %s",
                          self.endpoint_uri, method, response)
        return response

    def is_connected(self):
        try:
            self.logger.debug("Is connected")
            response = self.make_request('icx_getLastBlock', [])
            response = response
        except IOError:
            return False
        else:
            assert response['jsonrpc'] == '2.0'
            assert 'error' not in response
            return True

