# -*- coding: utf-8 -*-
# Copyright 2017-2018 ICON Foundation
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

from IconService.libs.serializer import serialize
from IconService.libs.signer import sign
from secp256k1 import PrivateKey
from .example_tx_requests import TEST_REQUEST_SCORE_FUNCTION_CALL, \
    TEST_REQUEST_SCORE_ISNTALL, TEST_REQUEST_SCORE_UPDATE, TEST_REQUEST_SEND_MESSAGE, \
    TEST_REQUEST_TRANSFER_ICX


class TestIcxSigner(unittest.TestCase):

    def test_verify_recoverable_sign(self):
        """Verifies recovering a signature."""

        test_requests = [TEST_REQUEST_TRANSFER_ICX, TEST_REQUEST_SCORE_FUNCTION_CALL,
                         TEST_REQUEST_SEND_MESSAGE, TEST_REQUEST_SCORE_UPDATE, TEST_REQUEST_SCORE_ISNTALL]

        for request in test_requests:
            # Serialize a signature
            private_key_object = PrivateKey()
            msg_hash_bytes = serialize(request["params"])
            sign_bytes = sign(msg_hash_bytes, private_key_object.private_key)

            # Deserialize a signature
            recoverable_sign = private_key_object.ecdsa_recoverable_deserialize(sign_bytes[0:64], sign_bytes[64])
            sign_ = private_key_object.ecdsa_recoverable_convert(recoverable_sign)
            # Verify a signature with a public key
            self.assertTrue(private_key_object.pubkey.ecdsa_verify(msg_hash_bytes, sign_, raw=True))

            # Verify a signature when an message is invalid
            invalid_msg_hash = hashlib.sha3_256(f'invalid message'.encode()).digest()
            self.assertFalse(private_key_object.pubkey.ecdsa_verify(invalid_msg_hash, sign_, raw=True))

            # Verify a signature when a private key is invalid
            invalid_private_key = PrivateKey()
            self.assertFalse(invalid_private_key.pubkey.ecdsa_verify(msg_hash_bytes, sign_, raw=True))


if __name__ == "__main__":
    unittest.main()









