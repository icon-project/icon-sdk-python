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

import re
from IconService.exception import AddressException, KeyStoreException
from .type import is_str
from .hexadecimal import is_0x_prefixed, remove_0x_prefix


def is_password_of_keystore_file(password) -> bool:
    """Validates a password.

    :param password: The password the user entering. type(str)
    :return: type(bool)
        True: When format of the password is valid.
        False: When format of the password is invalid.
    """
    return bool(re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+{}:<>?]).{8,}$', password))


def is_keystore_file(keystore: dict) -> bool:
    """Checks data in a keystore file is valid.

    :return: type(bool)
        True: When format of the keystore is valid.
        False: When format of the keystore is invalid.
    """

    root_keys = ["version", "id", "address", "crypto", "coinType"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]
    crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]

    is_valid = has_keys(keystore, root_keys) and has_keys(keystore["crypto"], crypto_keys)\
               and has_keys(keystore["crypto"]["cipherparams"], crypto_cipherparams_keys) \
               and has_keys(keystore["crypto"]["kdfparams"], crypto_kdfparams_keys)

    if is_valid:
        return is_valid
    else:
        raise KeyStoreException("The keystore file is invalid.")


def has_keys(target_data: dict, keys: list):
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


def is_wallet_address(address) -> bool:
    try:
        if len(address) == 42 and address.startswith('hx'):
            return True
        else:
            raise AddressException("An address is wrong.")
    except ValueError:
        raise AddressException("An address is wrong.")


def is_predefined_block_value(value) -> bool:
    """
    By far, predefined block value is only `latest`.
    Later it is possible to add others.

    :param value: "latest". type(str)
    :return: type(bool)
    """
    if is_str(value):
        value_text = value
    else:
        raise TypeError("It's unrecognized block reference:{0!r}.".format(value))

    return value_text == "latest"


def is_hex_block_hash(value) -> bool:
    """
    Checks the value - a parameter is valid.
    Hash value of a block starts with '0x' and 64 digits hex string

    :param value: hash value of a block, hexadecimal digits. type(str)
    :return: type(bool)
    """
    if not is_str(value):
        return False

    return is_0x_prefixed(value) and len(remove_0x_prefix(value)) == 64


def is_hex_block_height(value) -> bool:
    """Checks the value - a parameter is valid.

    :param value: height of a block, hexadecimal digits. type(str).
    :return: type(bool)
    """
    if not is_str(value):
        return False
    elif is_hex_block_hash(value):
        return False
    try:
        value_as_int = int(value, 16)
    except ValueError:
        return False
    return 0 <= value_as_int < 2 ** 256

