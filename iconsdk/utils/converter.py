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

import copy
import logging
import traceback

from iconsdk.exception import DataTypeException
from iconsdk.utils.hexadecimal import remove_0x_prefix
from iconsdk.utils.templates import (ValueType, ConvertKeyName, RemoveKey, ExceptionHandle, BLOCK_0_1a,
                                     TRANSACTIONS_OF_GENESIS_BLOCK)
from iconsdk.utils.type import is_str


def convert(return_value: dict, return_template, full_print: bool = False) -> dict:
    """
    Convert return value in dict into predefined return template

    by
    - converting key name,
    - its own type
    - removing key.

    :param return_value: return value from ICON JSON-RPC API v3
    :param return_template: predefined return template
    :param full_print: bool
        True is returning all keys of block template with emtpy string value
        False is returning existing keys and value
    :return: converted return value in dict as converted by key and removed
    """
    if isinstance(return_template, dict):
        if "CHANGE" in return_template:
            return_value = _change_key(return_value, return_template["CHANGE"])
        if full_print is True:
            buf_return_value = dict()
            for key, value in return_template.items():
                if key == "CHANGE":
                    continue
                buf_return_value[key] = return_value[key] if key in return_value else ""
            return_value = buf_return_value

    if isinstance(return_value, dict) and isinstance(return_template, dict):
        buf_return_value = dict()
        for key, value in return_value.items():
            buf_return_value[key] = convert(value, return_template.get(key, None))
    elif isinstance(return_value, list) and isinstance(return_template, list):
        buf_return_value = list()
        for item in return_value:
            buf_return_value.append(convert(item, return_template[0]))
    elif isinstance(return_template, ValueType):
        buf_return_value = convert_value(return_value, return_template) if return_value != '' else return_value
    else:
        buf_return_value = return_value

    return buf_return_value


def _change_key(obj, change_dict):
    new_obj = copy.copy(obj)
    for key, change_value in change_dict.items():
        if isinstance(change_value, RemoveKey):
            if key in new_obj:
                del new_obj[key]
        elif isinstance(change_value, ConvertKeyName):
            if key in new_obj:
                del new_obj[key]
                new_obj[change_value.new_key] = obj[key]
        elif isinstance(change_value, ExceptionHandle):
            if key in new_obj:
                change_value.func(key, new_obj[key], new_obj)
        else:
            raise RuntimeError(f"Not expected change, {change_value}")

    return new_obj


def convert_value(value, value_type):
    if value == '':
        return value
    try:
        if value_type == ValueType.str:
            return _to_str(value)
        elif value_type == ValueType.int:
            return _to_int(value)
        elif value_type == ValueType.bytes:
            return _to_bytes(value)
        elif value_type == ValueType.hex_hash_number:
            return _to_hex_hash_number(value)
        elif value_type == ValueType.prefixed_hex_hash_number:
            return _to_prefixed_hex_hash_number(value)

    except BaseException as e:
        traceback.print_exc()
        logging.error(f"Error : {e}, value : {value_type}:{value}")

    return value


def _to_str(value):
    if isinstance(value, str):
        return value
    return str(value)


def _to_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        if value.startswith('0x') or value.startswith('-0x'):
            return int(value, 16)
        try:
            return int(value)
        except:
            pass
        return int(value, 16)


def _to_bytes(value: str) -> bytes:
    """Converts hex string prefixed with '0x' into bytes."""
    if is_str(value):
        return bytes.fromhex(remove_0x_prefix(value))
    else:
        raise DataTypeException("Data type should be string.")


def _to_hex_hash_number(value):
    if isinstance(value, int):
        return hex(value).split("0x")[1]
    if isinstance(value, str):
        if value.startswith('0x') or value.startswith('-0x'):
            return value.split("0x")[1]
        else:
            return value


def _to_prefixed_hex_hash_number(value):
    if isinstance(value, int):
        return hex(value)
    if isinstance(value, str):
        if value.startswith('0x') or value.startswith('-0x'):
            return value

        num = int(value, 16)
        hex(int(value, 16))
        if num >= 0:
            return '0x' + value
        else:
            return '-0x' + value


def get_block_template_to_convert_transactions_for_genesis(block, block_template):
    buf_block_template = copy.deepcopy(block_template)
    if block["height"] == 0:
        buf_block_template["confirmed_transaction_list" if block_template == BLOCK_0_1a else "transactions"] \
            = TRANSACTIONS_OF_GENESIS_BLOCK
    return buf_block_template
