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
from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_icx_transaction, is_T_HASH
from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestSendTransfer(TestSendSuper):
    def test_transfer(self, _make_id):
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(3) \
            .nonce(self.setting["nonce"]) \
            .version(3) \
            .timestamp(self.setting["timestamp"]) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))
        signed_transaction = SignedTransaction(icx_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"

            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'value': hex(self.setting["value"]),
                    'version': '0x3'
                }
            }

            response_json: dict = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_invalid_transfer1(self, _make_id):
        # When value is wrong prefixed with '0x'
        wrong_value = "0x34330000000"
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(wrong_value) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .build()
        self.assertRaises(DataTypeException, SignedTransaction, icx_transaction, self.wallet)

    def test_invalid_transfer2(self, _make_id):
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"][2:]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .timestamp(self.setting["timestamp"]) \
            .build()
        signed_transaction = SignedTransaction(icx_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'from': self.setting["from"],
                    'to': self.setting["to"][2:],
                    'nid': hex(self.setting["nid"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'value': hex(self.setting["value"]),
                    'version': '0x3'
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Server error"
                },
                "id": 5
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", status_code=500, json=response_json)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
