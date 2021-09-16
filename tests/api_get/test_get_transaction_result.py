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
from unittest.mock import patch

import requests_mock

from iconsdk.exception import DataTypeException, JSONRPCException
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix
from iconsdk.utils.validation import is_transaction_result
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetTransactionResult(TestSendSuper):
    def test_get_transaction_result(self, _make_id):
        tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionResult',
                'params': {
                    'txHash': tx_hash
                }
            }
            response_json = {
                "jsonrpc": "2.0",
                "result": {
                    "txHash": "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388",
                    "blockHeight": "0x13f",
                    "blockHash": "0x069e8a2431ae2c7e55924af477be87518476aa1eb1b2e7d1ee8d61d7874ea907",
                    "txIndex": "0x1",
                    "to": "cx0000000000000000000000000000000000000000",
                    "stepUsed": "0x263b8",
                    "stepPrice": "0x2540be400",
                    "cumulativeStepUsed": "0x263b8",
                    "eventLogs": [
                        {
                            "scoreAddress": "cx0000000000000000000000000000000000000000",
                            "indexed": [
                                "PRepSet(Address)"
                            ],
                            "data": [
                                "hx86aba2210918a9b116973f3c4b27c41a54d5dafe"
                            ]
                        }
                    ],
                    "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000080000000000000000000000000000000000000000000000000000000000020000000000000008000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "status": "0x1"
                },
                "id": 1234
            }
            m.post(self.matcher, json=response_json)
            result = self.icon_service.get_transaction_result(tx_hash)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(is_transaction_result(result))

    def test_get_transaction_result_wrong_hash(self, _make_id):
        wrong_tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionResult',
                'params': {
                    'txHash': wrong_tx_hash
                }
            }
            response_json = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params txHash"
                },
                "id": 1234
            }
            m.post(self.matcher, json=response_json, status_code=400)
            # case 4: when tx_hash is invalid - not exist
            self.assertRaises(JSONRPCException, self.icon_service.get_transaction_result, wrong_tx_hash)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_get_transaction_result_invalid(self, _make_id):
        invalid_tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(
            DataTypeException,
            self.icon_service.get_transaction_result,
            remove_0x_prefix(invalid_tx_hash)
        )
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(
            DataTypeException,
            self.icon_service.get_transaction_result,
            add_cx_prefix(remove_0x_prefix(invalid_tx_hash))
        )
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(
            DataTypeException,
            self.icon_service.get_transaction_result,
            invalid_tx_hash[:15]
        )


if __name__ == "__main__":
    main()
