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

import requests_mock
import json

from unittest import main
from unittest.mock import patch
from tests.api_full_response.example_response import result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TesFullResponseGetTotalSupply(TestFullResponseBase):

    def test_get_total_supply(self, _make_id):
        with requests_mock.Mocker() as m:
            supply = 1_000_000_000
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTotalSupply',
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(supply),
                'id': 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result_dict = self.icon_service.get_total_supply(full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(result_success_v3.keys(), result_dict.keys())
            self.assertEqual(int(result_content, 16), supply)


if __name__ == "__main__":
    main()
