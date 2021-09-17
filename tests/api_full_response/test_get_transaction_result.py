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

from iconsdk.utils.validation import is_transaction_result
from tests.api_full_response.example_response import result_success_v3, result_error_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetTransactionResult(TestFullResponseBase):
    def test_get_transaction_result(self, _make_id):
        with requests_mock.Mocker() as m:
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionResult',
                'params': {
                    'txHash': self.transaction_hash
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": self.receipt,
                "id": 1234
            }
            m.post(self.matcher, json=response_json)
            result_dict = self.icon_service.get_transaction_result(self.transaction_hash, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(result_success_v3.keys(), result_dict.keys())
            self.assertTrue(is_transaction_result(result_content))

    def test_get_transaction_result_wrong_hash(self, _make_id):
        wrong_tx_hash: str = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        with requests_mock.Mocker() as m:
            response_json = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Invalid params txHash"
                },
                "id": 1234
            }

            m.post(self.matcher, json=response_json, status_code=400)
            result_dict = self.icon_service.get_block(wrong_tx_hash, full_response=True)
            self.assertEqual(result_dict.keys(), result_error_v3.keys())


if __name__ == "__main__":
    main()
