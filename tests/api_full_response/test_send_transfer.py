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
from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_message_transaction, is_T_HASH
from tests.api_full_response.example_response import result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestFullResponseSendTransfer(TestFullResponseBase):

    def test_send_transfer(self, _make_id):
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

        signed_transaction = SignedTransaction(icx_transaction, self.wallet)

        with requests_mock.Mocker() as m:
            response_json: dict = {
                "jsonrpc": "2.0",
                "result": "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238",
                "id": 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result_dict = self.icon_service.send_transaction(signed_transaction, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_content = result_dict['result']

            self.assertTrue(is_T_HASH(result_content))
            self.assertEqual(result_success_v3.keys(), result_dict.keys())


if __name__ == '__main__':
    main()
