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

import base64
import hashlib
from secp256k1 import PrivateKey


class IcxSigner:
    """Class for making a signature using a private key."""

    def __init__(self, private_key: bytes):
        self._private_key = private_key
        self._private_key_object = PrivateKey(self._private_key)

    def sign_recoverable(self, msg_hash: bytes):
        """Makes a recoverable signature using hash of a massage.
        Public key is extracted by a recoverable signature.

        :param msg_hash: Hash of a message. type(bytes)
        :return:
            type(tuple)
            type(bytes): 65 bytes data , type(int): recovery id
        """
        private_key_object = self._private_key_object
        recoverable_signature = private_key_object.ecdsa_sign_recoverable(msg_hash, raw=True)
        return private_key_object.ecdsa_recoverable_serialize(recoverable_signature)

    def sign(self, msg_hash: bytes) -> bytes:
        """Makes a recoverable signature data which type is base64-encoded string.

        :param msg_hash:
        :return a recoverable signature: type(str)
        """
        signature, recovery_id = self.sign_recoverable(msg_hash)
        recoverable_sig = bytes(bytearray(signature) + recovery_id.to_bytes(1, 'big'))
        return base64.b64encode(recoverable_sig)

    @property
    def public_key(self) -> bytes:
        return self._private_key_object.pubkey.serialize(compressed=False)

    @property
    def address(self) -> bytes:
        return hashlib.sha3_256(self.public_key[1:]).digest()[-20:]
