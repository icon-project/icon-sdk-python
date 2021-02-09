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

from unittest.mock import patch
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST
from iconsdk.builder.transaction_builder import MessageTransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_message_transaction, is_T_HASH, is_transaction_result, is_block
from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestSendMessage(TestSendSuper):

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
            result = self.icon_service.send_transaction(signed_transaction)
            self.assertTrue(is_T_HASH(result))
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_get_transaction_result(self, _make_id):
        with requests_mock.Mocker() as m:
            tx_hash = "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388"
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTransactionResult',
                'params': {
                    'txHash': tx_hash
                }
            }

            response_json = {
                "jsonrpc": "2.0",
                "result": {
                    "txHash": "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388",
                    "blockHeight": "0x13f",
                    "blockHash": "0x069e8a2431ae2c7e55924af477be87518476aa1eb1b2e7d1ee8d61d7874ea907",
                    "txIndex": "0x1",
                    "to": self.setting['to'],
                    "stepUsed": "0x263b8",
                    "stepPrice": "0x2540be400",
                    "cumulativeStepUsed": "0x263b8",
                    "eventLogs": [],
                    "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000080000000000000000000000000000000000000000000000000000000000020000000000000008000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                    "status": "0x1"
                },
                "id": 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.get_transaction_result(tx_hash)
            self.assertTrue(is_transaction_result(result))

            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)

    def test_get_block(self, _make_id):
        with requests_mock.Mocker() as m:
            response_json = {
                "jsonrpc": "2.0",
                "result": {
                    "version": "0.5",
                    "height": int('0x13f', 16),
                    "signature": "yO4YWy0+pM6IFad3exORZWhFD+4RLNSmhCwzIc5aJ3wfazGJH2e2sBWtGRDjiVK+xnw7SDWVUzik/aq3DmJLeQE=",
                    "prev_block_hash": "6399543b290eef968b68f88459190a4d6aedba1a3fafcc5169dc20184d01932a",
                    "merkle_tree_root_hash": "72bd9b1572a608e9108c285fbe7b34e3e814a1b263dd76065bd90e5b43d390f3",
                    "time_stamp": 1612856659125677,
                    "confirmed_transaction_list": [
                        {
                            "version": "0x3",
                            "timestamp": "0x5bae2743da5ad",
                            "dataType": "base",
                            "data": {
                                "prep": {
                                    "irep": "0x21e19e0c9bab2400000",
                                    "rrep": "0x1b0",
                                    "totalDelegation": "0x105e700bc013de49eb56d3e",
                                    "value": "0x2b2609c5e9b67ee3"
                                },
                                "result": {
                                    "coveredByFee": "0x228c61981e4800",
                                    "coveredByOverIssuedICX": "0x0",
                                    "issue": "0x2b037d64519836e3"
                                }
                            },
                            "txHash": "0xd92cce2a115d74544f2561db73a7b525cbb11b2cc95c0691acedfa2cd637fe44"
                        },
                        {
                            "version": "0x3",
                            "from": self.setting['from'],
                            "to": self.setting['to'],
                            "value": self.setting['value'],
                            "stepLimit": self.setting['step_limit'],
                            "nid": self.setting['nid'],
                            "timestamp": self.setting['nid'],
                            "nonce": self.setting['nonce'],
                            "signature": "gc5mS40dRlqs7qndNDhOZFDU/V6KpGAWc10zcXM4ukp1p7sCFKkMzJY0dVmzxIyE67cW8ybbcgjUa/Bp+yf0JwE=",
                            "txHash": "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388",
                            'data': self.setting['data']
                        }
                    ],
                    "block_hash": "1ad6d9651bc6038ff330cda87ddefecfa7674d441a4aa7de164237ad43006e22",
                    "peer_id": "hx49ce06eab947cb5ba2475781044d305af9d8d9d5",
                    "next_leader": "hx49ce06eab947cb5ba2475781044d305af9d8d9d5"
                },
                "id": 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result = self.icon_service.get_block(int('0x13f', 16))
            self.assertTrue(is_block(result))
            self.assertEqual(result["confirmed_transaction_list"][1]["data"], self.setting["data"])

    def test_invalid(self, _make_id):
        # When data is not hex string
        with requests_mock.Mocker() as m:
            message_transaction = MessageTransactionBuilder() \
                .from_(self.setting["from"]) \
                .to(self.setting["to"]) \
                .step_limit(self.setting["step_limit"]) \
                .nid(self.setting["nid"]) \
                .nonce(self.setting["nonce"]) \
                .data("test")

            # Raise DataTypeException
            self.assertRaises(DataTypeException, message_transaction.build)

            response_json = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32602,
                    "message": "Server error"
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json, status_code=400)
            # When address is wrong
            message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"][2:]) \
                .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
            signed_transaction = SignedTransaction(message_transaction, self.wallet)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)

            # When not having a required property, nid
            message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"][2:]) \
                .step_limit(self.setting["step_limit"]).data(self.setting["data"]).build()
            signed_transaction = SignedTransaction(message_transaction, self.wallet)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)

            # When a sending address is wrong - not the wallet's address
            message_transaction = MessageTransactionBuilder().from_(self.setting["to"]).to(self.setting["to"]) \
                .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
            signed_transaction = SignedTransaction(message_transaction, self.wallet)
            self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction)
