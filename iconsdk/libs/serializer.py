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

from copy import deepcopy
from hashlib import sha3_256
from typing import Optional

translator = str.maketrans({
    "\\": "\\\\",
    "{": "\\{",
    "}": "\\}",
    "[": "\\[",
    "]": "\\]",
    ".": "\\."
})


def __make_params_serialized(json_data: dict) -> str:

    def encode(data) -> str:
        if isinstance(data, dict):
            return encode_dict(data)
        elif isinstance(data, list):
            return encode_list(data)
        else:
            return escape(data)

    def encode_dict(data: dict) -> str:
        result = ".".join(_encode_dict(data))
        return "{" + result + "}"

    def _encode_dict(data: dict) -> list:
        for key in sorted(data.keys()):
            yield key
            yield encode(data[key])

    def encode_list(data: list) -> str:
        result = ".".join(_encode_list(data))
        return f"[" + result + "]"

    def _encode_list(data: list) -> list:
        for item in data:
            yield encode(item)

    def escape(data) -> str:
        if data is None:
            return "\\0"

        data = str(data)
        return data.translate(translator)

    return ".".join(_encode_dict(json_data))


def serialize(params: dict) -> bytes:
    """
    Serialized params of an original JSON request starting with `icx_sendTransaction`
    to generate a message hash for a signature.

    :param params: params in a original JSON request for transaction.
    :return: serialized params.
    For example, data like `icx_sendTransaction.<key1>.<value1>.<key2>.<value2>` is converted to bytes.
    """
    copy_tx = deepcopy(params)
    key_name_for_tx_hash = __get_key_name_for_tx_hash(params)

    if key_name_for_tx_hash in copy_tx:
        del copy_tx[key_name_for_tx_hash]

    if 'signature' in copy_tx:
        del copy_tx['signature']

    partial_serialized_params = __make_params_serialized(copy_tx)
    return f"icx_sendTransaction.{partial_serialized_params}".encode()


def generate_message(params: dict) -> str:
    """
    Generates transaction's message hash from params in request for transaction.

    :param params: params in request for transaction.
    :return: the 256 bit hash digest of a message. Hexadecimal encoded.
    """
    bytes_message_hash = serialize(params)
    return sha3_256(bytes_message_hash).hexdigest()


def __get_key_name_for_tx_hash(params: dict) -> Optional[str]:
    if __get_tx_version(params) == hex(2):
        return "tx_hash"
    else:
        return None


def __get_tx_version(params: dict) -> str:
    if 'version' not in params:
        return hex(2)
    else:
        return params['version']
