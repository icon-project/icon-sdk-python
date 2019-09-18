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

from typing import Union
import json
import os
from json.decoder import JSONDecodeError
from urllib.parse import urlparse

import requests
from multipledispatch import dispatch

from iconsdk import logger
from iconsdk.exception import JSONRPCException, URLException
from iconsdk.providers.config_api_path import CONFIG_API_PATH
from iconsdk.providers.provider import Provider
from iconsdk.utils import to_dict


class HTTPProvider(Provider):
    """
    The HTTPProvider takes the full URI where the server can be found.
    For local development this would be something like 'http://localhost:9000'.
    """

    @staticmethod
    def _validate_base_domain_url(base_domain_url: str) -> bool:
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
            logger.error(f"While setting HTTPProvider, raised URLException because the URL is invalid. "
                         f"URL: {base_domain_url}")
            raise URLException("Invalid base domain URL. "
                               "Valid base domain URL format is as like <scheme>://<host>:<port>.")
        self._full_path_url = None
        self._base_domain_url = base_domain_url
        self._version = version
        self._request_kwargs = request_kwargs or {}
        logger.info(f"Set HTTPProvider. "
                    f"Base domain URL: {base_domain_url}, Version: {version}, Request kwargs: {self._request_kwargs}")

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
        logger.info(f"Set HTTPProvider. "
                    f"Full path URL: {full_path_url}, Request kwargs: {self._request_kwargs}")

    def __str__(self):
        return "RPC connection {0}".format(self._base_domain_url)

    @to_dict
    def _get_request_kwargs(self) -> dict:
        if 'headers' not in self._request_kwargs:
            yield 'headers', {'Content-Type': 'application/json'}
        for key, value in self._request_kwargs.items():
            yield key, value

    @staticmethod
    def _make_post_request(full_path_url: str, data: dict, **kwargs) -> requests.Response:
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

    def make_request(self, method: str, params=None, full_response: bool = False) -> Union[str, list, dict]:
        rpc_dict = {
            'jsonrpc': '2.0',
            'method': method,
            'id': 1234
        }

        if params:
            rpc_dict['params'] = params

        full_path_url = self._full_path_url if self._full_path_url else self._get_full_path_url(method)
        response = self._make_post_request(full_path_url, rpc_dict, **self._get_request_kwargs())
        custom_response = self._return_custom_response(response, full_response)

        logger.debug(f"Request: {rpc_dict}")
        logger.debug(f"Response: {custom_response}")

        return custom_response

    @staticmethod
    def _return_custom_response(response: requests.Response, full_response: bool = False) -> Union[str, list, dict]:
        if full_response:
            return json.loads(response.content)

        if response.ok:
            content_as_dict = json.loads(response.content)
            return content_as_dict["result"]
        else:
            try:
                content_as_dict = json.loads(response.content)
            except (JSONDecodeError, KeyError):
                logger.exception(f"Raised URLException while returning the custom response. "
                                 f"Response content: {response.content.decode('utf-8')}")
                raise URLException(response.content.decode("utf-8"))
            else:
                logger.error(f"Raised JSONRPCException while returning the custom response. "
                             f"Error message: {content_as_dict['error']}")
                raise JSONRPCException(content_as_dict["error"])

    def is_connected(self) -> bool:
        try:
            logger.debug("Connected")
            last_block = self.make_request('icx_getLastBlock', [])
        except (IOError, URLException, JSONRPCException):
            return False
        else:
            return True
