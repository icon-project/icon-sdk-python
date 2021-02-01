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

from unittest import main

from iconsdk.exception import URLException
<<<<<<< HEAD
from iconsdk.providers.config_api_path import CONFIG_API_PATH
=======
from iconsdk.icon_service import IconService
>>>>>>> master
from iconsdk.providers.http_provider import HTTPProvider
from tests.api_send.test_send_super import TestSendSuper


class TestHTTPProvider(TestSendSuper):
    FULL_PATH_URL = "http://localhost:9000/api/v3"
    DEBUG_FULL_PATH_URL = "http://localhost:9000/api/debug/v3"
    BASE_PATH_URL = "http://localhost:9000"
    VERSION = 3
<<<<<<< HEAD
    request_kwargs: dict = {
        'timeout': 60,
        'allow_redirects': False,
        'verify': True
    }

    def test_http_provider_base_url(self):
        provider = HTTPProvider(
            self.BASE_PATH_URL,
            self.VERSION,
            request_kwargs=self.request_kwargs
        )
        self.assertEqual(self.BASE_PATH_URL, provider._base_domain_url)
        self.assertEqual(None, provider._full_path_url)
        self.assertEqual(self.VERSION, provider._version)
        self.assertEqual(self.request_kwargs, provider._request_kwargs)

        # debug
        for method in CONFIG_API_PATH:
            url: str = provider._get_full_path_url(method=method)
            self.assertEqual(self.DEBUG_FULL_PATH_URL, url)

    def test_http_provider_full_url(self):
        provider = HTTPProvider(
            self.FULL_PATH_URL,
            request_kwargs=self.request_kwargs
        )
        self.assertEqual(provider._full_path_url, self.FULL_PATH_URL)
        self.assertEqual(provider._request_kwargs, self.request_kwargs)

    def test_set_http_provider_validate_base_url(self):
=======

    def test_set_http_provider_with_param(self):
        # the initializer
        icon_service = IconService(HTTPProvider(self.FULL_PATH_URL))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

        # the new initializer
        icon_service = IconService(HTTPProvider(self.BASE_PATH_URL, self.VERSION))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

    def test_set_http_provider_with_request_kwargs(self):
        # the legacy initializer
        try:
            HTTPProvider(self.FULL_PATH_URL,
                         request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        except URLException:
            self.fail(f'Unexpected exception')

        # the new initializer to be failed
        with self.assertRaises(URLException):
            HTTPProvider(self.BASE_PATH_URL,
                         request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})

        # the new initializer to be success
        try:
            HTTPProvider(self.BASE_PATH_URL, 3,
                         request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        except URLException:
            self.fail(f'Unexpected exception')

    def test_set_http_provider_by_the_initializer_with_valid_url(self):
        """The initializer should pass all kind of URLs"""
        valid_urls = [
            "http://localhost:9000/api/v3",
            "https://ctz.solidwallet.io/api/v3",
            "http://localhost:9000/api/v3/channel"
        ]
        for url in valid_urls:
            try:
                HTTPProvider(url)
            except URLException:
                self.fail(f'Unexpected exception with {url}')

    def test_set_http_provider_by_new_initializer_with_invalid_url(self):
>>>>>>> master
        invalid_urls = [
            "http://localhost:9000/",
            "http://localhost:9000/api/v3",
            "http://localhost:9000/api/v3/",
            "http://localhost:9000/api/v3/channel",
            "https://ctz.solidwallet.io/",
            "https://ctz.solidwallet.io/api/v3",
        ]
<<<<<<< HEAD
        for invalid_url in invalid_urls:
            with self.assertRaises(URLException):
                HTTPProvider(invalid_url, self.VERSION)
=======
        for url in invalid_urls:
            with self.assertRaises(URLException):
                HTTPProvider(url, self.VERSION)
>>>>>>> master


if __name__ == "__main__":
    main()
