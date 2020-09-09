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

from iconsdk.builder.transaction_builder import MessageTransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_message_transaction, is_T_HASH
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class TestSendMessage(TestSendSuper):
    def test_send_message(self):
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data(self.setting["data"]) \
            .timestamp(self.setting["timestamp"]) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(message_transaction)
        self.assertTrue(is_message_transaction(tx_dict))
        # Checks if sending transaction correctly
        signed_transaction = SignedTransaction(message_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': self.setting["data"],
                    'dataType': 'message',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'version': '0x3'
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=expected_result)
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_send_message_invalid_data1(self):
        # When data is not hex string
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data("test")
        # Raise DataTypeException
        self.assertRaises(DataTypeException, message_transaction.build)

    def test_send_message_invalid_data2(self):
        message_transaction = MessageTransactionBuilder()\
            .from_(self.setting["from"]) \
            .to(self.setting["to"][2:]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .data(self.setting["data"]) \
            .timestamp(self.setting["timestamp"]) \
            .build()

        signed_transaction = SignedTransaction(message_transaction, self.wallet)
        with requests_mock.Mocker() as m:
            expected_result: dict = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Server error"
                },
                "id": 1234
            }
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': self.setting["data"],
                    'dataType': 'message',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"][2:],
                    'version': '0x3'
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", status_code=500, json=expected_result)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_send_message_invalid_data3(self):
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .data(self.setting["data"]) \
            .timestamp(self.setting["timestamp"]) \
            .build()

        signed_transaction = SignedTransaction(message_transaction, self.wallet)
        with requests_mock.Mocker() as m:
            expected_result: dict = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Server error"
                },
                "id": 1234
            }
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': self.setting["data"],
                    'dataType': 'message',
                    'from': self.setting["from"],
                    'nid': hex(1),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'version': '0x3'
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", status_code=500, json=expected_result)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
