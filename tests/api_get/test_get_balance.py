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
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST
from iconsdk.exception import AddressException
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetBalance(TestSendSuper):

    def test_get_balance_from_wallet(self, _make_id):
        # case 0: get balance from wallet or score successfully.
        with requests_mock.Mocker() as m:
            expected_result = 0
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBalance',
                'params': {
                    'address': self.setting["from"]
                }
            }
            response_json = {
                "jsonrpc": "2.0",
                "result": hex(0),
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.get_balance(self.setting["from"])
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertEqual(expected_result, result)

    def test_get_balance_invalid(self, _make_id):
        # case 1: when a param is wrong.
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["to"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["from"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, "123")
        self.assertRaises(AddressException, self.icon_service.get_balance, 123)
        # when the address's length is short
        self.assertRaises(AddressException, self.icon_service.get_balance, "cx882efc17c2f50e0d60142b9c0e746cbafb569d")


if __name__ == "__main__":
    main()
