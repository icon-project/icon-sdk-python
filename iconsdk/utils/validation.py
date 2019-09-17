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

from iconsdk.exception import KeyStoreException, DataTypeException
from iconsdk.utils.hexadecimal import (
    is_0x_prefixed,
    remove_0x_prefix,
    is_cx_prefixed,
    remove_cx_prefix,
    is_hx_prefixed,
    remove_hx_prefix
)
from iconsdk.utils.type import is_str, is_integer


def is_keystore_file(keystore: dict) -> bool:
    """Checks data in a keystore file is valid.

    :return: type(bool)
        True: When format of the keystore is valid.
        False: When format of the keystore is invalid.
    """

    root_keys = ["version", "id", "address", "crypto", "coinType"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]

    is_valid = has_keys(keystore, root_keys) and has_keys(keystore["crypto"], crypto_keys) \
               and has_keys(keystore["crypto"]["cipherparams"], crypto_cipherparams_keys)

    if is_valid:
        return is_valid
    else:
        raise KeyStoreException("The keystore file is invalid.")


def has_keys(target_data: dict, keys: list) -> bool:
    """Checks to a target data for having all of keys in list."""
    for key in keys:
        if key not in target_data.keys():
            return False
    return True


def is_keystore_file_for_icon(keystore: dict) -> bool:
    """
    Checks to a keystore for not eth but icon.
    1. Checks that a value of a key 'address' starts with 'hx'.
    2. Checks that a value of a key 'coinType' is same as 'icx'
    """
    if is_wallet_address(keystore["address"]) and keystore["coinType"] == "icx":
        return True
    else:
        raise KeyStoreException("The keystore file is invalid.")


def is_wallet_address(value) -> bool:
    """
    Checks if value is T_ADDR_EOA type.
    T_ADDR_EOA is data type which is 40-digit hexadecimal string prefixed with `hx`.

    :param value: wallet address
    """
    return is_str(value) and value.islower() and is_hx_prefixed(value) and len(remove_hx_prefix(value)) == 40


def is_score_address(value) -> bool:
    """
    Checks if value is T_ADDR_SCORE type.
    T_ADDR_SCORE is data type which is 40-digit hexadecimal string prefixed with `cx`.

    :param value: SCORE address
    """
    return is_str(value) and value.islower() and is_cx_prefixed(value) and len(remove_cx_prefix(value)) == 40


def is_T_HASH(value) -> bool:
    """T_HASH is data type which is 64-digit hexadecimal string prefixed with `0x`."""
    try:
        if is_0x_prefixed(value) and len(remove_0x_prefix(value)) == 64:
            return True
        else:
            raise DataTypeException("This hash value is unrecognized.")
    except ValueError:
        raise DataTypeException("This hash value is unrecognized.")


def is_T_BIN_DATA(value) -> bool:
    """
    T_BIN_DATA is data type which is hexadeciamal string prefixed with `0x`
    and length is even.
    """
    try:
        if is_0x_prefixed(value) and len(remove_0x_prefix(value)) % 2 == 0:
            return True
        else:
            raise DataTypeException("This value is not T_BIN_DATA data type.")
    except ValueError:
        raise DataTypeException("This value is not T_BIN_DATA data type.")


def is_predefined_block_value(value) -> bool:
    """
    By far, predefined block value is only `latest`.
    Later it is possible to add others.

    :param value: "latest". type(str)
    :return: type(bool)
    """
    return is_str(value) and value == "latest"


def is_hex_block_hash(value) -> bool:
    """
    Checks the value - a parameter is valid.
    Hash value of a block starts with '0x' and 64 digits hex string

    :param value: hash value of a block, hexadecimal digits. type(str)
    :return: type(bool)
    """
    return is_str(value) and is_0x_prefixed(value) and len(remove_0x_prefix(value)) == 64


def is_block_height(value: int) -> bool:
    """Checks the value - a parameter is valid.

    :param value: height of a block, hexadecimal digits. type(str).
    :return: type(bool)
    """
    try:
        if not is_integer(value):
            return False
    except ValueError:
        return False
    return 0 <= value < 2 ** 256


def is_block(result: dict) -> bool:
    """Checks block information in response has right format.

    :param result
    :return: bool
    """
    inner_key_of_result = ["version", "prev_block_hash", "merkle_tree_root_hash", "time_stamp",
                           "confirmed_transaction_list", "block_hash", "height", "peer_id", "signature"]
    return has_keys(result, inner_key_of_result)


def is_score_apis(result: dict) -> bool:
    """Checks list of score apis in response has right format.

    :param result
    :return: bool
    """
    result = result[0]
    inner_key_of_result = ["type", "name", "inputs", "outputs"]
    inner_key_of_inputs = ["name", "type"]
    return has_keys(result, inner_key_of_result) and has_keys(result["inputs"][0], inner_key_of_inputs)


def is_transaction(result: dict) -> bool:
    """Checks the result of `icx_getTransactionByHash` has right format.

    :param result
    :return: bool
    """
    inner_key_of_result = ["version", "from", "to", "stepLimit", "timestamp", "nid", "txIndex",
                           "blockHeight", "blockHash", "signature"]
    return has_keys(result, inner_key_of_result)


def is_transaction_result(result: dict) -> bool:
    """Checks the result of `icx_getTransactionResult` has right format.

    :param result
    :return: bool
    """
    inner_key_of_result = ["status", "to", "txHash", "txIndex", "blockHeight", "blockHash",
                           "cumulativeStepUsed", "stepUsed", "stepPrice"]
    return has_keys(result, inner_key_of_result)


def is_basic_transaction(params: dict) -> bool:
    """
    Checks an instance of `Transaction` has right format.
    Every types of `Transaction` like icx transaction, deploy transaction, call transaction and message transaction
    is checked by this method.
    """
    inner_key_of_params = ['version', 'from', 'to', 'stepLimit', 'timestamp', 'nid']

    return has_keys(params, inner_key_of_params) \
           and is_wallet_address(params['from']) \
           and (is_wallet_address(params['to']) or is_score_address(params['to'])) \
           and is_0x_prefixed(params['stepLimit']) \
           and is_0x_prefixed(params['timestamp']) is not None


def is_icx_transaction(params: dict) -> bool:
    """Checks an instance of `Transaction` for transfer icx has right format."""
    return is_basic_transaction(params) \
           and 'value' in params \
           and is_0x_prefixed(params['value'])


def is_deploy_transaction(params: dict) -> bool:
    """Checks an instance of `DeployTransaction` has right format."""
    inner_key_of_params = ['dataType', 'data']
    inner_key_of_data = ['contentType', 'content']

    return is_basic_transaction(params) \
           and has_keys(params, inner_key_of_params) \
           and has_keys(params['data'], inner_key_of_data) \
           and params['dataType'] == 'deploy' \
           and is_0x_prefixed(params['data']['content']) \
           and 'value' not in params


def is_call_transaction(params: dict) -> bool:
    """Checks an instance of `CallTransaction` has right format."""
    inner_key_of_params = ['dataType', 'data']
    inner_key_of_data = ['method']
    return is_basic_transaction(params) \
           and has_keys(params, inner_key_of_params) \
           and has_keys(params["data"], inner_key_of_data) \
           and params["dataType"] == "call"


def is_message_transaction(params: dict) -> bool:
    """Checks an instance of `MessageTransaction` has right format."""
    inner_key_of_params = ['dataType', 'data']
    return is_basic_transaction(params) \
           and has_keys(params, inner_key_of_params) \
           and is_0x_prefixed(params["data"]) \
           and params["dataType"] == "message"


def is_deposit_transaction(params: dict, deposit_type: str) -> bool:
    """Checks an instance of `DepositTransaction` has right format.

    :param params:
    :param deposit_type: add or withdraw
    :return: bool
    """
    inner_key_of_params = ['dataType', 'data']
    inner_key_of_data_for_add_action = ["action"]
    inner_key_of_data_for_withdraw_action = ["action", "id"]

    checked: bool = has_keys(params, inner_key_of_params) and params["dataType"] == "deposit"

    if deposit_type == "withdraw":
        return has_keys(params["data"], inner_key_of_data_for_withdraw_action) \
               and is_0x_prefixed(params["data"]["id"]) and params["data"]["action"] == "withdraw" and checked
    else:
        return has_keys(params["data"], inner_key_of_data_for_add_action) \
               and params["data"]["action"] == "add" and checked
