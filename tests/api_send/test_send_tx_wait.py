# -*- coding: utf-8 -*-
# Copyright 2021 ICON Foundation
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
from unittest.mock import patch

import requests_mock

from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_icx_transaction, is_T_HASH
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestSendAndWait(TestSendSuper):

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
                'method': 'icx_sendTransactionAndWait',
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
            m.post(self.matcher, json=response_json)
            self.icon_service.send_transaction_and_wait(signed_transaction)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
