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
from time import sleep
from unittest import main

import requests_mock

from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_cx_prefix
from iconsdk.utils.validation import is_transaction
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestGetTransactionByHash(TestSendSuper):
    def test_get_transaction_by_hash(self):
        tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionByHash',
                'params': {
                    'txHash': tx_hash
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "from": "hx0ed5504bd944ba047f37a84e511fe206dbd28493",
                    "to": "hxcf05607f22e27183b4908497d20b7a4496bd062c",
                    "value": "0x470de4df820000",
                    "fee": "0x2386f26fc10000",
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
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.get_transaction(tx_hash)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_invalidate_transaction1(self):
        invalid_tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        with requests_mock.Mocker() as m:
            expected_result: dict = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params txHash"
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", status_code=400, json=expected_result)
            # case 4: when tx_hash is invalid - not exist
            self.assertRaises(JSONRPCException, self.icon_service.get_transaction, invalid_tx_hash)

    def test_invalidate_transaction2(self):
        tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        # case 1: when tx_hash is invalid - no prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, remove_0x_prefix(tx_hash))
        # case 2: when tx_hash is invalid - wrong prefixed
        self.assertRaises(DataTypeException, self.icon_service.get_transaction,
                          add_cx_prefix(remove_0x_prefix(tx_hash)))
        # case 3: when tx_hash is invalid - too short
        self.assertRaises(DataTypeException, self.icon_service.get_transaction, tx_hash[:15])


if __name__ == "__main__":
    main()
