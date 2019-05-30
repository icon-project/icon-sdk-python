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

import os
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
        invalid_urls = ["http://localhost:9000/api/v2", "http://localhost:9000/api/v", "http://localhost:9000/api/",
                        "http://localhost:9000", "http://localhost:9000/api/debug/v3"]
        for invalid_url in invalid_urls:
            self.assertRaises(URLException, HTTPProvider, invalid_url)

    def test_set_http_provider_py_previous_initializer_with_valid_url(self):
        valid_url1 = "http://localhost:9000/api/v3"

        # When request kwargs is None
        with self.assertWarns(Warning):
            http_provider = HTTPProvider(valid_url1)
        self.assertEqual({}, http_provider._request_kwargs)

        # Checks full path url correctly
        full_path_url_for_main_api = "http://localhost:9000/api/v3"
        full_path_url_for_debug_api = "http://localhost:9000/api/debug/v3"
        self.assertEqual(full_path_url_for_main_api, http_provider._get_full_path_url("icx_call"))
        self.assertEqual(full_path_url_for_debug_api, http_provider._get_full_path_url("debug_estimateStep"))

        # When request kwargs is
        request_kwargs = {'timeout': 60, 'allow_redirects': False, 'verify': True}
        with self.assertWarns(Warning):
            http_provider = HTTPProvider(valid_url1, request_kwargs=request_kwargs)
        self.assertEqual(request_kwargs, http_provider._request_kwargs)

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

    def test_set_http_provider_by_previous_initializer_with_channel(self):
        full_path_url = "http://localhost:9000/api/v3/icon_dex"
        self.assertRaises(URLException, HTTPProvider, full_path_url)

        full_path_url_for_main_api = "http://localhost:9000/api/v3"
        full_path_url_for_debug_api = "http://localhost:9000/api/debug/v3"
        channel = "icon_dex"

        http_provider = HTTPProvider(full_path_url_for_main_api)
        self.assertTrue(http_provider.is_connected())

        # set channel
        http_provider.set_channel(channel)
        self.assertEqual(os.path.join(full_path_url_for_main_api, channel),
                         http_provider._get_full_path_url("icx_call"))
        self.assertEqual(os.path.join(full_path_url_for_debug_api, channel),
                         http_provider._get_full_path_url("debug_estimateStep"))

        # set the other channel
        channel = "icon_dex2"
        http_provider.set_channel(channel)
        self.assertEqual(os.path.join(full_path_url_for_main_api, channel),
                         http_provider._get_full_path_url("icx_call"))
        self.assertEqual(os.path.join(full_path_url_for_debug_api, channel),
                         http_provider._get_full_path_url("debug_estimateStep"))

    def test_set_http_provider_by_new_initializer_with_channel(self):
        base_domain_url = "http://localhost:9000"
        version = 3
        channel = "icon_dex"
        http_provider = HTTPProvider(base_domain_url, version)
        self.assertTrue(http_provider.is_connected())

        full_path_url_for_main_api = "http://localhost:9000/api/v3"
        full_path_url_for_debug_api = "http://localhost:9000/api/debug/v3"

        self.assertEqual(full_path_url_for_main_api, http_provider._get_full_path_url("icx_getTransactionByHash"))
        self.assertEqual(full_path_url_for_main_api, http_provider._get_full_path_url("icx_call"))
        self.assertEqual(full_path_url_for_debug_api, http_provider._get_full_path_url("debug_estimateStep"))

        # set channel
        http_provider.set_channel(channel)
        self.assertEqual(os.path.join(full_path_url_for_main_api, channel),
                         http_provider._get_full_path_url("icx_call"))
        self.assertEqual(os.path.join(full_path_url_for_debug_api, channel),
                         http_provider._get_full_path_url("debug_estimateStep"))

        # set the other channel
        channel = "icon_dex2"
        http_provider.set_channel(channel)
        self.assertEqual(os.path.join(full_path_url_for_main_api, channel),
                         http_provider._get_full_path_url("icx_call"))
        self.assertEqual(os.path.join(full_path_url_for_debug_api, channel),
                         http_provider._get_full_path_url("debug_estimateStep"))


if __name__ == "__main__":
    main()
