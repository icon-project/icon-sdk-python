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

import base64
from secp256k1 import PrivateKey, PublicKey


def sign(msg_hash: bytes, private_key_object: PrivateKey) -> bytes:
    """
    Create on ECDSA-SHA256 signature in bytes using massage hash.
    It refers to a document on https://github.com/ludbb/secp256k1-py.

    :param msg_hash: message hash: type(bytes)
    :param private_key_object:
    :return signature: type(bytes)
    """
    recoverable_sign = private_key_object.ecdsa_sign_recoverable(msg_hash, raw=True)
    sign_bytes, sign_recovery = private_key_object.ecdsa_recoverable_serialize(recoverable_sign)
    return sign_bytes + sign_recovery.to_bytes(1, 'big')


def sign_b64encode(sign_bytes: bytes) -> str:
    """Return a base64 encoding signature.

    :param sign_bytes:
    :return:
    """
    return base64.b64encode(sign_bytes)
