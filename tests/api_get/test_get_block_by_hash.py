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
from iconsdk.utils.hexadecimal import remove_0x_prefix
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetBlockByHash(TestSendSuper):

    def test_get_block_by_hash(self, _make_id):
        with requests_mock.Mocker() as m:
            block_hash = "0x033f8d96045eb8301fd17cf078c28ae58a3ba329f6ada5cf128ee56dc2af26f7"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBlockByHash',
                'params': {
                    'hash': block_hash
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": {
                    "version": "0.1a",
                    "prev_block_hash": "cf43b3fd45981431a0e64f79d07bfcf703e064b73b802c5f32834eec72142190",
                    "merkle_tree_root_hash": "375540830d475a73b704cf8dee9fa9eba2798f9d2af1fa55a85482e48daefd3b",
                    "time_stamp": 1516819217223222,
                    "confirmed_transaction_list": [
                        {
                            "from": "hx54f7853dc6481b670caf69c5a27c7c8fe5be8269",
                            "to": "hx49a23bd156932485471f582897bf1bec5f875751",
                            "value": "0x56bc75e2d63100000",
                            "fee": "0x2386f26fc10000",
                            "nonce": "0x1",
                            "tx_hash": "375540830d475a73b704cf8dee9fa9eba2798f9d2af1fa55a85482e48daefd3b",
                            "signature": "bjarKeF3izGy469dpSciP3TT9caBQVYgHdaNgjY+8wJTOVSFm4o/ODXycFOdXUJcIwqvcE9If8x6Zmgt//XmkQE=",
                            "method": "icx_sendTransaction"
                        }
                    ],
                    "block_hash": "3add53134014e940f6f6010173781c4d8bd677d9931a697f962483e04a685e5c",
                    "height": 1,
                    "peer_id": "hx7e1a1ece096ef3fa44ac9692394c2e11d0017e4a",
                    "signature": "liAIa7aPYvBRdZAdBz6zt2Gc9vVo/4+gkDz5uscS8Mw+B5gkp6zQeHhD5sNpyWcIsq5c9OxwOCUaBp0vu8eAgwE=",
                    "next_leader": ""
                },
                "id": 1234
            }

            # case 0: when hash value of latest block is valid
            m.post(self.matcher, json=response_json)
            result = self.icon_service.get_block(block_hash)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result)

            # case 1: when hash value is invalid not prefixed with `0x`
            invalid_hash = remove_0x_prefix(block_hash)
            self.assertRaises(DataTypeException, self.icon_service.get_block, invalid_hash)

    def test_get_block_by_wrong_hash(self, _make_id):
        with requests_mock.Mocker() as m:
            invalid_block_hash = "0x033f8d96045eb8301fd17cf078c28ae58a3ba329f6ada5cf128ee56dc2af26f7"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getBlockByHash',
                'params': {
                    'hash': invalid_block_hash
                }
            }

            response_json = {
                'id': 1234,
                "jsonrpc": "2.0",
                "error": {
                     "code": -32602,
                     "message": "fail wrong block hash"
                 },
            }
            m.post(self.matcher, json=response_json, status_code=400)
            self.assertRaises(JSONRPCException, self.icon_service.get_block, invalid_block_hash)
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)


if __name__ == "__main__":
    main()
