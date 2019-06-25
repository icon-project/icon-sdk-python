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

from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.exception import URLException, JSONRPCException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from tests.api_send.test_send_super import TestSendSuper


class TestHTTPProvider(TestSendSuper):
    FULL_PATH_URL = "http://localhost:9000/api/v3"
    DEBUG_FULL_PATH_URL = "http://localhost:9000/api/debug/v3"
    BASE_PATH_URL = "http://localhost:9000"
    VERSION = 3

    def test_set_http_provider_with_param(self):
        # the initializer
        icon_service = IconService(HTTPProvider(self.FULL_PATH_URL))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

        # the new initializer
        icon_service = IconService(HTTPProvider(self.BASE_PATH_URL, self.VERSION))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

    def test_set_http_provider_with_request_kwargs(self):
        # the initializer
        http_provider = HTTPProvider(self.FULL_PATH_URL,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertTrue(http_provider.is_connected())

        # the new initializer to be failed
        http_provider = HTTPProvider(self.BASE_PATH_URL,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertFalse(http_provider.is_connected())

        # the new initializer to be success
        http_provider = HTTPProvider(self.BASE_PATH_URL, 3,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertTrue(http_provider.is_connected())

    def test_set_http_provider_by_the_initializer_with_valid_url(self):
        """The initializer should pass all kind of URLs"""
        valid_urls = [
            "http://localhost:9000/api/v2",
            "http://localhost:9000/api/v",
            "http://localhost:9000/api/",
            "http://localhost:9000",
            "http://localhost:9000/api/debug/v3"
        ]
        for valid_url in valid_urls:
            icon_service = IconService(HTTPProvider(valid_url))

    def test_call_api_by_the_initializer_with_valid_url(self):
        http_provider = HTTPProvider(self.FULL_PATH_URL)
        self.assertIsNotNone(http_provider._full_path_url)
        try:
            http_provider._base_domain_url
        except AttributeError:
            self.assertTrue(True)

        icon_service = IconService(http_provider)
        self.assertEqual(type(icon_service.get_block("latest")), dict)

    def test_call_api_by_the_initializer_with_invalid_url(self):
        http_provider = HTTPProvider(self.DEBUG_FULL_PATH_URL)  # invalid URL
        self.assertIsNotNone(http_provider._full_path_url)

        icon_service = IconService(http_provider)
        self.assertRaises(JSONRPCException, icon_service.get_block, "latest")

    def test_call_debug_api_by_initializer_with_valid_url(self):
        http_provider = HTTPProvider(self.DEBUG_FULL_PATH_URL)
        self.assertIsNotNone(http_provider._full_path_url)
        try:
            http_provider._base_domain_url
        except AttributeError:
            self.assertTrue(True)

        icon_service = IconService(http_provider)

        # When having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(3) \
            .nonce(self.setting["nonce"]) \
            .version(self.VERSION) \
            .build()

        self.assertEqual(100000, icon_service.estimate_step(icx_transaction))

    def test_call_debug_api_by_initializer_with_invalid_url(self):
        http_provider = HTTPProvider(self.FULL_PATH_URL)
        self.assertIsNotNone(http_provider._full_path_url)
        try:
            http_provider._base_domain_url
        except AttributeError:
            self.assertTrue(True)

        icon_service = IconService(http_provider)

        # When having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(3) \
            .nonce(self.setting["nonce"]) \
            .version(self.VERSION) \
            .build()

        self.assertRaises(JSONRPCException, icon_service.estimate_step, icx_transaction)

    def test_set_http_provider_by_new_initializer_with_invalid_url(self):
        invalid_urls = [
            "http://localhost:9000/api/v3/channel",
            "localhost",
            "http://localhost:9000/api/v3"
        ]
        for invalid_url in invalid_urls:
            try:
                http_provider = HTTPProvider(invalid_url, self.VERSION)
                icon_service = IconService(http_provider)
            except URLException:
                self.assertTrue(True)
            else:
                self.assertFalse(True)

    def test_set_http_provider_by_initializer_with_channel(self):
        full_path_url_with_channel = "http://localhost:9000/api/v3/icon_dex"
        http_provider = HTTPProvider(full_path_url_with_channel)
        self.assertEqual(http_provider._full_path_url, full_path_url_with_channel)
        try:
            http_provider._base_domain_url
        except AttributeError:
            self.assertTrue(True)


if __name__ == "__main__":
    main()
