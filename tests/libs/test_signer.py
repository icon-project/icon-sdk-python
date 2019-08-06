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

from coincurve import PrivateKey, PublicKey

from iconsdk.libs.serializer import serialize
from iconsdk.libs.signer import sign
from tests.example_tx_requests import (
    TEST_REQUEST_TRANSFER_ICX,
    TEST_REQUEST_SCORE_FUNCTION_CALL,
    TEST_REQUEST_SEND_MESSAGE,
    TEST_REQUEST_SCORE_UPDATE,
    TEST_REQUEST_SCORE_ISNTALL
)


class TestIcxSigner(TestCase):

    def test_verify_recoverable_sign(self):
        """Verifies recovering a signature."""

        test_requests = [
            TEST_REQUEST_TRANSFER_ICX,
            TEST_REQUEST_SCORE_FUNCTION_CALL,
            TEST_REQUEST_SEND_MESSAGE,
            TEST_REQUEST_SCORE_UPDATE,
            TEST_REQUEST_SCORE_ISNTALL
        ]

        for request in test_requests:
            # Serialize a signature
            private_key_object: PrivateKey = PrivateKey()
            private_key_bytes: bytes = private_key_object.secret

            msg = serialize(request["params"])
            message_hash = sha3_256(msg).digest()
            sign_bytes = sign(message_hash, private_key_bytes)

            public_key = PublicKey.from_signature_and_message(sign_bytes, message_hash, hasher=None)
            self.assertEqual(public_key.format(), private_key_object.public_key.format())


if __name__ == "__main__":
    main()
