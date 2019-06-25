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
import os
from json.decoder import JSONDecodeError
from logging import getLogger
from urllib.parse import urlparse

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

    _logger = getLogger("HTTPProvider")

    # No need to use logging, remove the line.
    # set_logger(logger, 'DEBUG')

    @staticmethod
    def _validate_base_domain_url(base_domain_url) -> bool:
        """
        Validates if input base domain url is valid or not.

        When base domain url is as below,
        <scheme>://<host>:<port>
        if there are scheme and netloc which are host and port, it returns True.

        :param base_domain_url: as like <scheme>://<host>:<port>
        :return: True or False
        """
        url_components = urlparse(base_domain_url)
        if all([url_components.scheme, url_components.netloc]) and url_components.path in ('', '/'):
            return True
        else:
            return False

    @dispatch(str, int, dict=None)
    def __init__(self, base_domain_url: str, version: int, request_kwargs: dict = None):
        """
        The initializer to be set with base domain URL and version.

        :param base_domain_url: base domain URL as like <scheme>://<host>:<port>
        :param version: version for RPC server
        :param request_kwargs: kwargs for setting to head of request
        """
        if not self._validate_base_domain_url(base_domain_url):
            raise URLException("Invalid base domain URL. "
                               "Valid base domain URL format is as like <scheme>://<host>:<port>.")
        self._full_path_url = None
        self._base_domain_url = base_domain_url
        self._version = version
        self._request_kwargs = request_kwargs or {}

    @dispatch(str, dict=None)
    def __init__(self, full_path_url: str, request_kwargs: dict = None):
        """
        The initializer to be set with full path url as like <scheme>://<host>:<port>/api/v3.
        If you need to use a channel, you can use it such as <scheme>://<host>:<port>/api/v3/{channel}.

        :param full_path_url: full path URL as like <scheme>://<host>:<port>/api/v3
        :param request_kwargs: kwargs for setting to head of request
        """
        self._full_path_url = full_path_url
        self._request_kwargs = request_kwargs or {}

    def __str__(self):
        return "RPC connection {0}".format(self._base_domain_url)

    @to_dict
    def _get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield 'headers', {'Content-Type': 'application/json'}
        for key, value in self._request_kwargs.items():
            yield key, value

    @staticmethod
    def _make_post_request(full_path_url, data, **kwargs):
        kwargs.setdefault('timeout', 10)
        with requests.Session() as session:
            response = session.post(url=full_path_url, data=json.dumps(data), **kwargs)
        return response

    def _get_full_path_url(self, method: str) -> str:
        url_components = urlparse(self._base_domain_url)
        if method in CONFIG_API_PATH:
            path = os.path.join(CONFIG_API_PATH[method], 'v' + str(self._version))
        else:
            path = os.path.join("api", "v" + str(self._version))
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

        full_path_url = self._full_path_url if self._full_path_url else self._get_full_path_url(method)
        response = self._make_post_request(full_path_url, rpc_dict, **self._get_request_kwargs())

        # self._logger.debug("request HTTP\nURI: %s\nMethod: %s\nData: %s", full_path_url, method, rpc_dict)
        # self._logger.debug("response HTTP\nResponse:%s", response)

        return self._return_customed_response(response)

    @staticmethod
    def _return_customed_response(response):
        if response.ok:
            content_as_dict = json.loads(response.content)
            return content_as_dict["result"]
        else:
            try:
                content_as_dict = json.loads(response.content)
            except (JSONDecodeError, KeyError):
                raise URLException(response.content.decode("utf-8"))
            else:
                raise JSONRPCException(content_as_dict["error"])

    def is_connected(self):
        try:
            # self._logger.debug("Connected")
            last_block = self.make_request('icx_getLastBlock', [])
        except (IOError, URLException, JSONRPCException):
            return False
        else:
            return True
