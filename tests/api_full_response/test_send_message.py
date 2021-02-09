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
from iconsdk.builder.transaction_builder import MessageTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_message_transaction, is_T_HASH
from tests.api_full_response.example_response import result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestFullResponseSendMessage(TestFullResponseBase):

    def test_send_message(self, _make_id):
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
        signed_transaction = SignedTransaction(message_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            tx_hash = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_sendTransaction',
                'params': {
                    'data': self.setting["data"],
                    'dataType': 'message',
                    'from': self.setting["from"],
                    'nid': hex(self.setting["nid"]),
                    'nonce': hex(self.setting["nonce"]),
                    'timestamp': hex(self.setting["timestamp"]),
                    'signature': signed_transaction.signed_transaction_dict["signature"],
                    'stepLimit': hex(self.setting["step_limit"]),
                    'to': self.setting["to"],
                    'version': hex(3)
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': tx_hash,
                'id': 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result_dict = self.icon_service.send_transaction(signed_transaction, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertTrue(is_T_HASH(result_content))
            self.assertEqual(result_success_v3.keys(), result_dict.keys())
            self.assertEqual(expected_request, actual_request)


if __name__ == '__main__':
    main()