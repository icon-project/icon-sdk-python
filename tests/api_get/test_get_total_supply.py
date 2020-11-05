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
from unittest import main

import requests_mock

from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestGetTotalSupply(TestSendSuper):
    def test_get_total_supply(self):
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTotalSupply',
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": hex(1_000_000),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.get_total_supply()
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)


if __name__ == "__main__":
    main()
