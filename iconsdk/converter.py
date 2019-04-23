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

from iconsdk.utils.convert_type import convert_hex_str_to_int, convert_hex_str_to_bytes
from iconsdk.utils.hexadecimal import add_0x_prefix, is_0x_prefixed
from iconsdk.utils.type import is_integer


def convert_transaction(transaction: dict):
    """
    Convert transaction data into the right format.
    It supports data about a transaction made not only from JSON RPC V3 but also from V2.

    [what to do on the method 'convert_common_data_on_transaction']
    1. Fields as value, fee, nid, stepLimit, timestamp, and nonce have to be converted to an integer.
    2. Fields as timestamp and nonce have a different type of the value by the version as V2 or V3.
        - If the version V3, the data type is hex string prefixed with '0x'.
        - If the version V2, the data type is a string but the meaning is an integer.
    3. The field 'method' has to be removed.
    4. The field 'version' has to be added number 2 if the version is 2 or if 3, has to be converted to an integer.
    5. If the field 'dataType' is 'deploy', the field 'content' has to be converted to bytes.
       Or if 'message', the field 'data' has to be converted to an integer.

    [Added]
    6. Fields as 'txIndex' and 'blockHeight' have to be converted to an integer.

    :param transaction: data about the single transaction
    """
    convert_common_data_on_transaction(transaction)

    # List of Fields which have to be converted to int
    int_fields = ["txIndex", "blockHeight"]

    for int_field in int_fields:
        if int_field in transaction:
            transaction[int_field] = convert_hex_str_to_int(transaction[int_field])


def convert_block(data: dict):
    """
    Convert block data into the right format.
    It supports data about a block made not only from JSON RPC V3 but also from V2.

    1. If the genesis block, don't convert data because we can not know what data format it is.
    2. Transaction list on a block has to be converted by the method 'convert_common_data_on_transaction' for each transaction.
       You can check what to do on the method in the docstring of the function 'convert_transaction'.
    3. The field name 'tx_hash' on the transaction made from JSON RPC V2 has to be converted to 'txHash'.
       Furthermore, the value of the field has to be prefixed with '0x'.

    :param data: data about the block
    """
    # Genesis block
    if data["height"] == 0:
        return data

    for transaction in data["confirmed_transaction_list"]:
        convert_common_data_on_transaction(transaction)

        if "tx_hash" in transaction:
            transaction["txHash"] = add_0x_prefix(transaction["tx_hash"])
            del transaction["tx_hash"]


def convert_common_data_on_transaction(transaction: dict):
    """
    Convert common fields in the transaction such as value, fee, nid, stepLimit, timestamp, nonce, method, version, data.
    Used in validating a transaction list in a block or validating a single transaction.

    1. Fields such as value, fee, nid, stepLimit, timestamp, and nonce have to be converted to an integer.
    2. Fields such as timestamp and nonce have a different type of the value by the version as V2 or V3.
        - If the version V3, the data type is hex string prefixed with '0x'.
        - If the version V2, the data type is a string but the meaning is an integer.
    3. The field 'method' has to be removed.
    4. The field 'version' has to be added number 2 if the version is 2 or if 3, has to be converted to an integer.
    5. If the field 'dataType' is 'deploy', the field 'content' has to be converted to bytes.

    :param transaction: data about the single transaction
    """

    # List of Fields which have to be converted to int
    int_fields = ["value", "fee", "nid", "stepLimit"]

    for int_field in int_fields:
        if int_field in transaction:
            transaction[int_field] = convert_hex_str_to_int(transaction[int_field])

    odd_fields = ["timestamp", "nonce"]

    for odd_field in odd_fields:
        if odd_field in transaction:
            if is_integer(transaction[odd_field]):
                pass
            elif is_0x_prefixed(transaction[odd_field]):
                transaction[odd_field] = convert_hex_str_to_int(transaction[odd_field])
            else:
                transaction[odd_field] = int(transaction[odd_field])

    if "method" in transaction:
        del transaction["method"]

    if "version" in transaction and convert_hex_str_to_int(transaction["version"]) >= 3:
        transaction["version"] = convert_hex_str_to_int(transaction["version"])
    else:
        transaction["version"] = 2

    if "dataType" in transaction:
        if transaction["dataType"] == "deploy":
            transaction["data"]["content"] = convert_hex_str_to_bytes(transaction["data"]["content"])


def convert_transaction_result(data: dict):
    """
    Convert transaction result data into the right format.
    It supports data about a transaction made not only from JSON RPC V3 but also from V2.

    1. Fields such as status, blockHeight, txIndex, stepUsed, stepPrice, cumulativeStepUsed have to be converted to an integer.
    2. The field 'logsBloom' has to be converted to bytes.

    :param data: data about the transaction result
    """
    # Only for the transaction made with JSON RPC V2 successfully does not have the property 'status'
    if "status" not in data and "code" in data and data["code"] == 0:
        data["status"] = 1
        del data["code"]
        return

    # List of Fields which have to be converted to int
    int_fields = ["status", "blockHeight", "txIndex", "stepUsed", "stepPrice", "cumulativeStepUsed"]

    for int_field in int_fields:
        if int_field in data:
            data[int_field] = convert_hex_str_to_int(data[int_field])

    if "logsBloom" in data:
        data["logsBloom"] = convert_hex_str_to_bytes(data["logsBloom"])



