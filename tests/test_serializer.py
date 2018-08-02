# -*- coding: utf-8 -*-
# Copyright 2017-2018 theloop Inc.
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

import unittest
import hashlib

from IconService.libs.serializer import generate_tx_hash, serialize_params_to_message_hash


class TestSerializer(unittest.TestCase):

    def test_for_serialize_case_for_sending_normal_tx(self):
        """Test when serializer serializes perfectly in this case when is normal send transaction."""
        tx_request = {
                        "jsonrpc": "2.0",
                        "method": "icx_sendTransaction",
                        "id": 1234,
                        "params": {
                            "version": "0x3",
                            "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
                            "value": "0xde0b6b3a7640000",
                            "stepLimit": "0x12345",
                            "timestamp": "0x563a6cf330136",
                            "nonce": "0x1",
                            "signature": "VAia7YZ2Ji6igKWzjR2YsGa2m53nKPrfK7uXYW78QLE+ATehAVZPC40szvAiA6NEU5gCYB4c4qaQzqDh2ugcHgA="
                            }
                     }

        params_of_tx_request = tx_request["params"]
        correct_serialized_params = "icx_sendTransaction.from.hxbe258ceb872e08851f1f59694dac2558708ece11." \
                                    "nonce.0x1.stepLimit.0x12345.timestamp.0x563a6cf330136.to.hx5bfdb090f" \
                                    "43a808005ffc27c25b213145e80b7cd.value.0xde0b6b3a7640000.version.0x3"

        self.assertEqual(correct_serialized_params.encode(), serialize_params_to_message_hash(params_of_tx_request))

    def test_for_serialize_case_for_calling(self):
        """Test when serializer serializes perfectly in this case when dataType is call."""
        tx_request = {
                        "jsonrpc": "2.0",
                        "method": "icx_sendTransaction",
                        "id": 1234,
                        "params": {
                            "version": "0x3",
                            "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                            "to": "cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32",
                            "stepLimit": "0x12345",
                            "timestamp": "0x563a6cf330136",
                            "nonce": "0x1",
                            "signature": "VAia7YZ2Ji6igKWzjR2YsGa2m53nKPrfK7uXYW78QLE+ATehAVZPC40szvAiA6NEU5gCYB4c4qaQzqDh2ugcHgA=",
                            "dataType": "call",
                            "data": {
                                "method": "transfer",
                                "params": {
                                    "to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
                                    "value": "0x1"
                                }
                            }
                        }
                    }

        params_of_tx_request = tx_request["params"]
        correct_serialized_params = "icx_sendTransaction.data.{method.transfer.params.{to.hxab2d8215eab14bc6bdd8b" \
                                    "fb2c8151257032ecd8b.value.0x1}}.dataType.call.from.hxbe258ceb872e08851f1f596" \
                                    "94dac2558708ece11.nonce.0x1.stepLimit.0x12345.timestamp.0x563a6cf330136.to.c" \
                                    "xb0776ee37f5b45bfaea8cff1d8232fbb6122ec32.version.0x3"
        self.assertEqual(correct_serialized_params.encode(), serialize_params_to_message_hash(params_of_tx_request))

    def test_for_checking_hash_is_correct_case_for_sending_normal_tx(self):
        """
        Test for checking the transaction hash is correct successfully
        in this case when is normal send transaction.
        """
        tx_request = {
                        "jsonrpc": "2.0",
                        "method": "icx_sendTransaction",
                        "id": 1234,
                        "params": {
                            "version": "0x3",
                            "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
                            "value": "0xde0b6b3a7640000",
                            "stepLimit": "0x12345",
                            "timestamp": "0x563a6cf330136",
                            "nonce": "0x1",
                            "signature": "VAia7YZ2Ji6igKWzjR2YsGa2m53nKPrfK7uXYW78QLE+ATehAVZPC40szvAiA6NEU5gCYB4c4qaQzqDh2ugcHgA="
                            }
                     }
        params_of_tx_request = tx_request["params"]
        tx_hash = generate_tx_hash(params_of_tx_request)
        correct_tx_hash = hashlib.sha3_256(serialize_params_to_message_hash(params_of_tx_request)).hexdigest()
        self.assertEqual(tx_hash, correct_tx_hash)

    def test_for_checking_hash_is_correct_case_for_calling(self):
        """Test for checking the transaction hash is correct successfully in this case when dataType is call."""
        tx_request = {
                        "jsonrpc": "2.0",
                        "method": "icx_sendTransaction",
                        "id": 1234,
                        "params": {
                            "version": "0x3",
                            "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                            "to": "cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32",
                            "stepLimit": "0x12345",
                            "timestamp": "0x563a6cf330136",
                            "nonce": "0x1",
                            "signature": "VAia7YZ2Ji6igKWzjR2YsGa2m53nKPrfK7uXYW78QLE+ATehAVZPC40szvAiA6NEU5gCYB4c4qaQzqDh2ugcHgA=",
                            "dataType": "call",
                            "data": {
                                "method": "transfer",
                                "params": {
                                    "to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
                                    "value": "0x1"
                                }
                            }
                        }
                    }
        params_of_tx_request = tx_request["params"]
        tx_hash = generate_tx_hash(params_of_tx_request)
        correct_tx_hash = hashlib.sha3_256(serialize_params_to_message_hash(params_of_tx_request)).hexdigest()
        self.assertEqual(tx_hash, correct_tx_hash)


if __name__ == "__main__":
    unittest.main()
