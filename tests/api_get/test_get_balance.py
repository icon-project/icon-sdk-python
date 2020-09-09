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

from iconsdk.exception import AddressException
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestGetBalance(TestSendSuper):
    def test_get_balance_from_wallet(self):
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBalance',
                'params': {
                    'address': self.setting["from"]
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": hex(0),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.get_balance(self.setting["from"])
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_balance_invalid_wallet(self):
        # case 1: when a param is wrong.
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["to"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["from"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, "123")
        self.assertRaises(AddressException, self.icon_service.get_balance, 123)
        # when the address's length is short
        self.assertRaises(AddressException, self.icon_service.get_balance, "cx882efc17c2f50e0d60142")


if __name__ == "__main__":
    main()
