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

from os import path
from unittest import TestCase, main
from IconService.wallet.wallet import KeyWallet
from IconService.exception import KeyStoreException


class TestWalletLoadFromKeystoreFile(TestCase):

    TEST_KEYSTORE_FILE_DIR = path.abspath("tests/keystore_file/test_keystore.txt")
    TEST_KEYSTORE_FILE_PASSWORD = "Adas21312**"
    TEST_DIR = path.abspath("keystore_file")

    def test_wallet_load_from_keystore_file(self):
        """A wallet loads from a keystore file correctly."""

        # Loads a wallet.
        wallet = KeyWallet.load(self.TEST_KEYSTORE_FILE_DIR, self.TEST_KEYSTORE_FILE_PASSWORD)

        # Checks a wallet's address is correct.
        self.assertEqual(wallet.get_address(), "hxfd7e4560ba363f5aabd32caac7317feeee70ea57")

    def test_wallet_load_from_invalid_directory(self):
        """Case when loading a wallet from a invalid directory not existing."""
        keystore_file_path = path.join(self.TEST_DIR, "unknown_folder", "test_keystore.txt")

        try:
            wallet = KeyWallet.load(keystore_file_path, self.TEST_KEYSTORE_FILE_PASSWORD)
        except FileNotFoundError:
            self.assertTrue(True)

    def test_wallet_load_with_invalid_password(self):
        """Case When loading a wallet with a invalid password."""
        password = "1234wrongpassword"
        self.assertRaises(KeyStoreException, KeyWallet.load, self.TEST_KEYSTORE_FILE_DIR, password)


if __name__ == "__main__":
    main()
