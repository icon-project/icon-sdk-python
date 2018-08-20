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
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3


class TestHTTPProvider(TestCase):

    def test_set_http_provider_with_param(self):
        icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        self.assertEqual(type(icon_service.get_block("latest")), dict)

    def test_set_http_provider_with_request_kwargs(self):
        http_provider = HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3,
                                     request_kwargs={'timeout': 60, 'allow_redirects': False, 'verify': True})
        self.assertTrue(http_provider.is_connected())


if __name__ == "__main__":
    main()
