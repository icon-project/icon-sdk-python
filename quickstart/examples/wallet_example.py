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

from iconsdk.wallet.wallet import KeyWallet
from quickstart.examples.test.constant import TEST_PRIVATE_KEY

# Generates a wallet
wallet1 = KeyWallet.create()
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

wallet2 = KeyWallet.load(TEST_PRIVATE_KEY)
print("[wallet2] address: ", wallet2.get_address(), " private key: ", wallet2.get_private_key())

# Removes the file if exists
file_path = "./test/test_keystore"
if path.isfile(file_path):
    remove(file_path)

# Stores a key store file on the file path
wallet1.store(file_path, "abcd1234*")

# Loads a wallet from a key store file
wallet1 = KeyWallet.load("./test/test_keystore", "abcd1234*")
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

