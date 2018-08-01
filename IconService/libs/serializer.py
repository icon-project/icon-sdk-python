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
import copy
import hashlib


class IcxSerializer:

    translator = str.maketrans({
        "\\": "\\\\",
        "{": "\\{",
        "}": "\\}",
        "[": "\\[",
        "]": "\\]",
        ".": "\\."
    })

    def __make_params_serialized(self, json_data: dict):

        def encode(data):
            if isinstance(data, dict):
                return encode_dict(data)
            elif isinstance(data, list):
                return encode_list(data)
            else:
                return escape(data)

        def encode_dict(data: dict):
            result = ".".join(_encode_dict(data))
            return "{" + result + "}"

        def _encode_dict(data: dict):
            for key in sorted(data.keys()):
                yield key
                yield encode(data[key])

        def encode_list(data: list):
            result = ".".join(_encode_list(data))
            return f"[" + result + "]"

        def _encode_list(data: list):
            for item in data:
                yield encode(item)

        def escape(data):
            if data is None:
                return "\\0"

            data = str(data)
            return data.translate(self.translator)

        return ".".join(_encode_dict(json_data))

    def __get_key_name_for_tx_hash(self, params_in_JSON_request):
        if self.__get_tx_version(params_in_JSON_request) == hex(3):
            key_name_for_tx_hash = "txHash"
        else:
            key_name_for_tx_hash = "tx_hash"
        return key_name_for_tx_hash

    def __get_tx_version(self, params_in_JSON_request):
        if 'version' in params_in_JSON_request and params_in_JSON_request['version'] == hex(3):
            return hex(3)
        return hex(2)

    def serialize(self, params_in_JSON_request):
        """It Serialized params of an original JSON request. It starts the method name, "icx_sendTransaction".

        :param params_in_JSON_request:
        :return: serialized params. Like icx_sendTransaction.<key1>.<value1>.<key2>.<value2>.
        """
        copy_tx = copy.deepcopy(params_in_JSON_request)

        key_name_for_tx_hash = self.__get_key_name_for_tx_hash(params_in_JSON_request)
        if key_name_for_tx_hash in copy_tx:
            del copy_tx[key_name_for_tx_hash]

        if 'method' in copy_tx:
            del copy_tx['method']

        if 'signature' in copy_tx:
            del copy_tx['signature']

        partial_serialized_params = self.__make_params_serialized(copy_tx)
        return f"icx_sendTransaction.{partial_serialized_params}"


def generate_tx_hash(params_in_JSON_request: dict):
    """
    It generates transaction's hash with params in an original JSON request for transaction.
    The point is serialization is applied on params field value, a dictionary.

    :param params_in_JSON_request: params in a original JSON request for transaction.
    :return: the 256 bit hash digest of a message. Hexadecimal encoded.
    """
    full_serialized_params = IcxSerializer().serialize(params_in_JSON_request)
    return hashlib.sha3_256(full_serialized_params.encode()).hexdigest()
