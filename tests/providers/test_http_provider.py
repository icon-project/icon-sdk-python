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

from unittest import TestCase, main

from iconsdk.exception import URLException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3


class TestHTTPProvider(TestCase):

    def test_set_http_provider_with_param(self):
        icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

    def test_set_http_provider_with_request_kwargs(self):
        http_provider = HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertTrue(http_provider.is_connected())

    def test_set_http_provider_by_previous_initializer_with_invalid_url(self):
        invalid_url0 = "http://localhost:9000/api/v2"
        invalid_url1 = "http://localhost:9000/api/v"
        invalid_url2 = "http://localhost:9000/api/"
        invalid_url3 = "http://localhost:9000"
        self.assertRaises(URLException, HTTPProvider, invalid_url0)
        self.assertRaises(URLException, HTTPProvider, invalid_url1)
        self.assertRaises(URLException, HTTPProvider, invalid_url2)
        self.assertRaises(URLException, HTTPProvider, invalid_url3)

    def test_set_http_provider_by_new_initializer_with_invalid_url(self):
        invalid_url0 = "localhost:9000"
        invalid_url1 = "localhost"
        version = 3
        self.assertRaises(URLException, HTTPProvider, invalid_url0, version)
        self.assertRaises(URLException, HTTPProvider, invalid_url1, version)

    def test_set_http_provider_by_new_initializer_with_valid_url(self):
        valid_url = "http://localhost:9000"
        version = 3
        http_provider = HTTPProvider(valid_url, version)
        self.assertTrue(http_provider.is_connected())

        icon_service = IconService(HTTPProvider(valid_url, version))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

        http_provider = HTTPProvider(valid_url, version,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertTrue(http_provider.is_connected())
        icon_service = IconService(http_provider)
        self.assertEqual(type(icon_service.get_block("latest")), dict)


if __name__ == "__main__":
    main()
