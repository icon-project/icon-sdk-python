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
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix
from iconsdk.utils.validation import is_transaction
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetTransactionByHash(TestSendSuper):

    def test_get_transaction_by_hash(self, _make_id):
        with requests_mock.Mocker() as m:
            tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionByHash',
                'params': {
                    'txHash': tx_hash
                }
            }
            response_json = {
                "jsonrpc": "2.0",
                "result": {
                    "version": "0x3",
                    "from": self.setting["from"],
                    "to": self.setting["to"],
                    "stepLimit": hex(self.setting["step_limit"]),
                    "value": "0x470de4df820000",
                    "nid": hex(self.setting["nid"]),
                    "timestamp": "1517999520286000",
                    "signature": "sILBL1MPwOou8ItM4s0Vqx21l62QyucgTLsEQ51BGi5v/IJ1hOCT/P/rz1V1pDSGAnTQ7rGw9rSOVM5TAGbJOAE=",
                    "method": "icx_sendTransaction",
                    "txHash": tx_hash,
                    "txIndex": "0x0",
                    "blockHeight": "0xa",
                    "blockHash": "0x9a39a75d7075687f746d61191baf1a1ff3b5bc0acc4a8df0bb872e53e13cdc17"
                },
                "id": 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            # case 0: when tx_hash is valid
            result = self.icon_service.get_transaction(tx_hash)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(is_transaction(result))

    def test_get_transaction_invalid(self, _make_id):
        tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, remove_0x_prefix(tx_hash))
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction,
                          add_cx_prefix(remove_0x_prefix(tx_hash)))
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, tx_hash[:15])

    def test_get_transaction_wrong_hash(self, _make_id):
        with requests_mock.Mocker() as m:
            wrong_tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            response_json = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params txHash"
                },
                "id": 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json, status_code=400)
            self.assertRaises(JSONRPCException, self.icon_service.get_transaction, wrong_tx_hash)


if __name__ == "__main__":
    main()
