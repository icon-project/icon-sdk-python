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

from iconsdk.exception import DataTypeException, JSONRPCException
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestGetBlockByHeight(TestSendSuper):
    def test_get_block_by_height(self):
        with requests_mock.Mocker() as m:
            height: int = 1
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBlockByHeight',
                'params': {
                    'height': hex(height)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "version": "0.1a",
                    "prev_block_hash": "cf43b3fd45981431a0e64f79d07bfcf703e064b73b802c5f32834eec72142190",
                    "merkle_tree_root_hash": "375540830d475a73b704cf8dee9fa9eba2798f9d2af1fa55a85482e48daefd3b",
                    "time_stamp": 1516819217223222,
                    "confirmed_transaction_list": [
                        {
                            "from": "hx54f7853dc6481b670caf69c5a27c7c8fe5be8269",
                            "to": "hx49a23bd156932485471f582897bf1bec5f875751",
                            "value": "0x56bc75e2d63100000",
                            "fee": "0x2386f26fc10000",
                            "nonce": "0x1",
                            "tx_hash": "375540830d475a73b704cf8dee9fa9eba2798f9d2af1fa55a85482e48daefd3b",
                            "signature": "bjarKeF3izGy469dpSciP3TT9caBQVYgHdaNgjY+8wJTOVSFm4o/ODXycFOdXUJcIwqvcE9If8x6Zmgt//XmkQE=",
                            "method": "icx_sendTransaction"
                        }
                    ],
                    "block_hash": "3add53134014e940f6f6010173781c4d8bd677d9931a697f962483e04a685e5c",
                    "height": 1,
                    "peer_id": "hx7e1a1ece096ef3fa44ac9692394c2e11d0017e4a",
                    "signature": "liAIa7aPYvBRdZAdBz6zt2Gc9vVo/4+gkDz5uscS8Mw+B5gkp6zQeHhD5sNpyWcIsq5c9OxwOCUaBp0vu8eAgwE=",
                    "next_leader": ""
                },
                "id": 5
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.get_block(height)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_block_by_invalid_height1(self):
        overflow_height: int = 1
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBlockByHeight',
                'params': {
                    'height': hex(overflow_height)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "fail wrong block hash"
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", status_code=400, json=expected_result)
            self.assertRaises(JSONRPCException, self.icon_service.get_block, overflow_height)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_block_by_invalid_height2(self):
        self.assertRaises(DataTypeException, self.icon_service.get_block, "1")
        self.assertRaises(DataTypeException, self.icon_service.get_block, "0x123")
        self.assertRaises(DataTypeException, self.icon_service.get_block, -2)


if __name__ == "__main__":
    main()
