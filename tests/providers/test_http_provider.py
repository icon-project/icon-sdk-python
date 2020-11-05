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
from iconsdk.providers.config_api_path import CONFIG_API_PATH
from iconsdk.providers.http_provider import HTTPProvider
from tests.api_send.test_send_super import TestSendSuper


class TestHTTPProvider(TestSendSuper):
    FULL_PATH_URL = "http://localhost:9000/api/v3"
    DEBUG_FULL_PATH_URL = "http://localhost:9000/api/debug/v3"
    BASE_PATH_URL = "http://localhost:9000"
    VERSION = 3
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
        invalid_urls = [
            "http://localhost:9000/api/v3/channel",
            "localhost",
            "http://localhost:9000/api/v3"
        ]
        for invalid_url in invalid_urls:
            with self.assertRaises(URLException):
                HTTPProvider(invalid_url, self.VERSION)


if __name__ == "__main__":
    main()
