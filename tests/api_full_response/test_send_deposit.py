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

from iconsdk.builder.transaction_builder import DepositTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_T_HASH
from tests.api_full_response.example_response import result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TesFullResponseSendDeposit(TestFullResponseBase):
    def test_add_deposit(self, _make_id):
        # transaction instance for add action
        action = "add"
        deposit_transaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .timestamp(self.setting["timestamp"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action(action) \
            .build()
        signed_transaction = SignedTransaction(deposit_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': {
                        'action': action
                    },
                    'dataType': 'deposit',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'to': self.setting["to"],
                    'value': hex(self.setting["value"]),
                    'version': hex(3)
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": tx_hash,
                "id": 1234
            }
            m.post(self.matcher, json=response_json)
            result_dict = self.icon_service.send_transaction(signed_transaction, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(result_success_v3.keys(), result_dict.keys())
            self.assertTrue(is_T_HASH(result_content))


if __name__ == "__main__":
    main()
