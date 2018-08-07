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


def validate_password_of_keystore_file(password) -> bool:
    """Validates a password.

    :param password: The password the user entering. type(str)
    :return: type(bool)
        True: When format of the password is valid.
        False: When format of the password is invalid.
    """
    return bool(re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+{}:<>?]).{8,}$', password))


def validate_keystore_file(keystore: dict) -> bool:
    """Checks data in a keystore file is valid.

    :return: type(bool)
        T∂rue: When format of the keystore is valid.
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


def validate_keystore_file_is_for_icon(keystore: dict) -> bool:
    """
    Checks to a keystore for not eth but icon.
    1. Checks that a value of a key 'address' starts with 'hx'.
    2. Checks that a value of a key 'coinType' is same as 'icx'
    """
    if validate_address(keystore["address"]) and keystore["coinType"] == "icx":
        return True
    else:
        raise KeyStoreException("The keystore file is invalid.")


def validate_address(address) -> bool:
    try:
        if len(address) == 42 and address.startswith('hx'):
            return True
        else:
            raise AddressException("An address is wrong.")
    except ValueError:
        raise AddressException("An address is wrong.")
