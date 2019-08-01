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

from unittest import TestCase, main

from coincurve import PrivateKey

from iconsdk.utils.validation import is_wallet_address
from iconsdk.wallet.wallet import KeyWallet


class TestWalletLoadByPrivateKey(TestCase):

    def test_wallet_load_by_private_key(self):
        """A wallet loads by a private key correctly."""

        # Creates a wallet.
        private_key_object = PrivateKey()
        private_key: bytes = private_key_object.secret
        wallet1 = KeyWallet.load(private_key)

        # Checks a private key as same.
        self.assertEqual(private_key.hex(), wallet1.get_private_key())

        # Checks a wallet's address is correct.
        self.assertTrue(is_wallet_address(wallet1.get_address()))

        # Creates the other wallet.
        private_key_object2 = PrivateKey()
        private_key2: bytes = private_key_object2.secret
        wallet2 = KeyWallet.load(private_key2)

        # Checks a private key as same.
        self.assertEqual(private_key2.hex(), wallet2.get_private_key())

        # Checks a wallet's address is correct.
        self.assertTrue(is_wallet_address(wallet2.get_address()))

        self.assertNotEqual(private_key2, private_key)


if __name__ == "__main__":
    main()
