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

from os import path, remove
from unittest import TestCase, main

from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet


class TestWalletStore(TestCase):

    TEST_CUR_DIR = path.dirname(__file__)
    TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE = path.abspath(
        path.join(TEST_CUR_DIR, '../keystore_file/test_new_keystore.txt'))
    TEST_WRONG_PATH_OF_KEYSTORE_FILE = path.abspath(path.join(TEST_CUR_DIR, "../unknown_folder", "test_keystore.txt"))

    TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE = "Adas21312**"
    TEST_WRONG_PASSWORD_OF_KEYSTORE_FILE = "123456"

    def test_wallet_store_successfully(self):
        """Creates a wallet and validate the wallet."""
        wallet = KeyWallet.create()
        wallet.store(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE, self.TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE)
        wallet2 = wallet.load(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE, self.TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE)

        self.assertEqual(wallet.get_address(), wallet2.get_address())
        self.assertEqual(wallet.get_private_key(), wallet2.get_private_key())

    def test_wallet_store_on_the_wrong_path(self):
        """Case When storing a keystore file on a wrong path that does not exist."""
        wallet = KeyWallet.create()
        self.assertRaises(KeyStoreException, wallet.store, self.TEST_WRONG_PATH_OF_KEYSTORE_FILE,
                          self.TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE)

    def test_wallet_store_with_wrong_password(self):
        """Successful Case to store wallet even though entering a invalid password."""
        wallet = KeyWallet.create()
        wallet.store(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE, self.TEST_WRONG_PASSWORD_OF_KEYSTORE_FILE)

    def test_wallet_store_overwriting(self):
        """Case when overwriting the existing keystore file."""
        wallet = KeyWallet.create()
        wallet.store(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE, self.TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE)

        wallet2 = KeyWallet.create()
        self.assertRaises(KeyStoreException, wallet2.store, self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE,
                          self.TEST_RIGHT_PASSWORD_OF_KEYSTORE_FILE)

    def tearDown(self):
        # Remove used file.
        if path.isfile(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE):
            remove(self.TEST_RIGHT_PATH_OF_NEW_KEYSTORE_FILE)


if __name__ == "__main__":
    main()
