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
from logging import getLogger
from urllib.parse import urlparse
from warnings import warn

import requests
from multipledispatch import dispatch

from iconsdk.exception import JSONRPCException, URLException
from iconsdk.providers.config_api_path import CONFIG_API_PATH
from iconsdk.providers.provider import Provider
from iconsdk.utils import to_dict


class HTTPProvider(Provider):
    """
    The HTTPProvider takes the full URI where the server can be found.
    For local development this would be something like 'http://localhost:9000'.
    """
    endpoint_uri = None
    _request_kwargs = None

    logger = getLogger("HTTPProvider")

    # No need to use logging, remove the line.
    # set_logger(logger, 'DEBUG')

    @staticmethod
    def validate_base_domain_url(base_domain_url) -> bool:
        """
        Validates if input base domain url is valid or not.

        When base domain url is as below,
        <scheme>://<host>:<port>
        if there are scheme and netloc which are host and port, it returns True.

        :param base_domain_url: as like <scheme>://<host>:<port>
        :return: True or False
        """
        url_components = urlparse(base_domain_url)
        return True if all([url_components.scheme, url_components.netloc]) else False

    @dispatch(str, int, dict=None)
    def __init__(self, base_domain_url: str, version: int, request_kwargs: dict = None):
        """
        The new initializer to be set with base domain URL and version.

        :param base_domain_url: base domain URL as like <scheme>://<host>:<port>
        :param version: version for RPC server
        :param request_kwargs: kwargs for setting to head of request
        """
        if not self.validate_base_domain_url(base_domain_url):
            raise URLException("Invalid base domain URL. "
                               "Valid base domain URL format is as like <scheme>://<host>:<port>.")
        self.base_domain_url = base_domain_url
        self.version = version
        self._request_kwargs = request_kwargs or {}

    @dispatch(str, dict=None)
    def __init__(self, full_path_url: str, request_kwargs: dict = None):
        """
        The previous initializer to be set with full path url which is only as like <scheme>://<host>/api/v3 without version.

        :param full_path_url: full path URL as like <scheme>://<host>:<port>/api/v3
        :param request_kwargs: kwargs for setting to head of request
        """
        warn('This initializer is deprecated and replaced with new initializer '
             'where parameters are not only endpoint but also version.')
        url_components = urlparse(full_path_url)
        if url_components.path != '/api/v3':
            raise URLException("Invalid full path URL. "
                               "The only valid full path for the previous initializer is "
                               "'<scheme>://<host>:<port>/api/v3'.")
        self.__init__(url_components.geturl(), int(url_components.path[-1:]))
        self._request_kwargs = request_kwargs or {}

    def __str__(self):
        return "RPC connection {0}".format(self.base_domain_url)

    @to_dict
    def get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield 'headers', {'Content-Type': 'application/json'}
        for key, value in self._request_kwargs.items():
            yield key, value

    @staticmethod
    def make_post_request(full_path_url, data, **kwargs):
        kwargs.setdefault('timeout', 10)
        with requests.Session() as session:
            response = session.post(url=full_path_url, data=json.dumps(data), **kwargs)
        return json.loads(response.content)

    def get_full_path_url(self, method: str) -> str:
        url_components = urlparse(self.base_domain_url)
        if method in CONFIG_API_PATH:
            path = CONFIG_API_PATH[method] + '/v' + str(self.version)
        else:
            path = "/api/v" + str(self.version)
        url_components = url_components._replace(path=path)
        return url_components.geturl()

    def make_request(self, method, params=None):
        rpc_dict = {
            'jsonrpc': '2.0',
            'method': method,
            'id': 1234
        }

        if params:
            rpc_dict['params'] = params

        self.logger.debug("request HTTP\nURI: %s\nMethod: %s\nData: %s",
                          self.base_domain_url, method, rpc_dict)

        response = self.make_post_request(self.get_full_path_url(method), rpc_dict, **self.get_request_kwargs())
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
            self.make_request('icx_getLastBlock', [])
        except IOError:
            return False
        else:
            return True
