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

import unittest
from IconService.wallet.wallet import KeyWallet, get_public_key
from IconService.utils.validation import validate_address


class TestWalletCreate(unittest.TestCase):

    def test_wallet_create_successfully(self):
        """Case both of each wallets are created successfully without a private key."""
        wallet1 = KeyWallet.create()
        wallet2 = KeyWallet.create()
        self.assertTrue(wallet1.get_address() != wallet2.get_address())
        self.assertTrue(validate_address(wallet1.get_address()))
        self.assertTrue(validate_address(wallet2.get_address()))


if __name__ == "__main__":
    unittest.main()