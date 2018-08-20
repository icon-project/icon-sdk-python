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

from hashlib import sha3_256
from unittest import TestCase, main
from IconService.libs.serializer import serialize
from tests.example_tx_requests import TEST_REQUEST_TRANSFER_ICX, TEST_REQUEST_SCORE_FUNCTION_CALL


class TestSerializer(TestCase):

    def test_for_serialize_case_for_sending_normal_tx(self):
        """Test when serializer serializes perfectly in this case when is normal send transaction."""
        tx_request = TEST_REQUEST_TRANSFER_ICX
        correct_serialized_params = "icx_sendTransaction.from.hxbe258ceb872e08851f1f59694dac2558708ece11.nid.0x3f." \
                                    "nonce.0x1.stepLimit.0x12345.timestamp.0x563a6cf330136.to.hx5bfdb090f43a808005" \
                                    "ffc27c25b213145e80b7cd.value.0xde0b6b3a7640000.version.0x3"
        self.assertEqual(sha3_256(correct_serialized_params.encode()).digest(),
                         serialize(tx_request["params"]))

    def test_for_serialize_case_for_calling(self):
        """Test when serializer serializes perfectly in this case when dataType is call."""
        tx_request = TEST_REQUEST_SCORE_FUNCTION_CALL
        correct_serialized_params = "icx_sendTransaction.data.{method.transfer.params.{to.hxab2d8215eab14bc6bdd8b" \
                                    "fb2c8151257032ecd8b.value.0x1}}.dataType.call.from.hxbe258ceb872e08851f1f596" \
                                    "94dac2558708ece11.nid.0x3f.nonce.0x1.stepLimit.0x12345.timestamp.0x563a6cf33" \
                                    "0136.to.cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32.version.0x3"
        self.assertEqual(sha3_256(correct_serialized_params.encode()).digest(),
                         serialize(tx_request["params"]))


if __name__ == "__main__":
    main()
