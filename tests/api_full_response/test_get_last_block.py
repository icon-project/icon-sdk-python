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
import requests_mock

from unittest.mock import patch
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST
from unittest import main

from iconsdk.utils.validation import is_block
from tests.api_full_response.example_response import result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestFullResponseGetBlockByHeight(TestFullResponseBase):

    def test_get_last_block_full_response(self, _make_id):
        # used valid hash and got and valid block
        with requests_mock.Mocker() as m:
            expected_request = {
                'jsonrpc': '2.0',
                'method': 'icx_getLastBlock',
                'id': 1234,
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': self.block,
                'id': 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result_dict = self.icon_service.get_block("latest", full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_keys = result_dict.keys()
            result_content = result_dict['result']

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(result_success_v3.keys(), result_keys)
            self.assertTrue(is_block(result_content))


if __name__ == "__main__":
    main()