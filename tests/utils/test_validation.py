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

from os import path
from unittest import TestCase, main
from IconService.utils.validation import is_keystore_file, has_keys, is_keystore_file_for_icon
from eth_keyfile import load_keyfile
from IconService.exception import KeyStoreException


class TestValidation(TestCase):

    TEST_KEYSTORE_FILE_DIR = path.abspath("tests/keystore_file/test_keystore.txt")
    TEST_NOT_KEYSTORE_FILE_DIR = path.abspath("tests/keystore_file/not_a_keystore_file.txt")

    def test_method_validate_keystore_file(self):
        """Case when validating a keystore file correctly. """
        keystore = load_keyfile(self.TEST_KEYSTORE_FILE_DIR)
        self.assertTrue(is_keystore_file(keystore))
        keystore = load_keyfile(self.TEST_NOT_KEYSTORE_FILE_DIR)
        self.assertRaises(KeyStoreException, is_keystore_file, keystore)

    def test_method_has_keys(self):
        """Case when a dictionary data in a keystore file have all of keys correctly. """
        target_data = {
                            'address': 'hxfd7e4560ba363f5aabd32caac7317feeee70ea57',
                            'crypto': {
                                'cipher': 'aes-128-ctr',
                                'cipherparams': {
                                    'iv': '952dc6c2e7d4ed5df45f4ddeac817dfb'
                                },
                                'ciphertext': 'c5482f14fcdae4848b74be65593452efe11c106fac2fe82801cb7735d5fa9b55',
                                'kdf': 'pbkdf2',
                                'kdfparams': {
                                    'c': 262144,
                                    'dklen': 32,
                                    'prf': 'hmac-sha256',
                                    'salt': '65fa9a3d6e8991a01f883990b0b0ca91'
                                },
                                'mac': '380e8daf36daff0e02949e4a40c0c8263890978071f0794581025b8e41e589a4'
                            },
                            'id': 'dd9fd4f9-3279-42d1-96f1-9ef637ddb6e6',
                            'version': 3,
                            'coinType': 'icx'
                        }

        root_keys = ["version", "id", "address", "crypto", "coinType"]
        crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
        crypto_cipherparams_keys = ["iv"]
        crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]

        self.assertTrue(has_keys(target_data, root_keys))
        self.assertTrue(has_keys(target_data["crypto"], crypto_keys))
        self.assertTrue(has_keys(target_data["crypto"]["cipherparams"], crypto_cipherparams_keys))
        self.assertTrue(has_keys(target_data["crypto"]["kdfparams"], crypto_kdfparams_keys))

    def test_validate_keystore_file_is_for_icon(self):
        """Case when validating keystore file if for icon or not."""
        keystore = load_keyfile(self.TEST_KEYSTORE_FILE_DIR)
        self.assertTrue(is_keystore_file_for_icon(keystore))

        # when an address's length is too short.
        keystore["address"] = "hx123"
        self.assertRaises(KeyStoreException, is_keystore_file_for_icon, keystore)

        # when an address doesn't start with 'hx'.
        keystore["address"] = "axfd7e4560ba363f5aabd32caac7317feeee70ea57"
        self.assertRaises(KeyStoreException, is_keystore_file_for_icon, keystore)

        # when an value of key 'coinType' is not same as 'icx'.
        keystore["address"] = "hxfd7e4560ba363f5aabd32caac7317feeee70ea57"
        keystore["coinType"] = "ic"
        self.assertRaises(KeyStoreException, is_keystore_file_for_icon, keystore)


if __name__ == "__main__":
    main()
