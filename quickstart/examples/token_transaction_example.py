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
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.utils.convert_type import convert_hex_str_to_int
from quickstart.examples.test.constant import TEST_HTTP_ENDPOINT_URI_V3, TEST_PRIVATE_KEY, GOVERNANCE_ADDRESS


def get_default_step_cost():
    call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getStepCosts")\
        .build()
    _result = icon_service.call(call)
    default_step_cost = convert_hex_str_to_int(_result["default"])
    print(default_step_cost)
    return default_step_cost


icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))

wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)

# Loads a wallet from a key store file
wallet2 = KeyWallet.load("./test/test_keystore", "abcd1234*")
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

params = {"_to": wallet2.get_address(), "_value": 10}

score_address = "cxa755b2ef6eb46c1e817c636be3c21d26c81fe6cc"

call_transaction = CallTransactionBuilder()\
    .from_(wallet1.get_address())\
    .to(score_address) \
    .step_limit(get_default_step_cost()*2)\
    .nid(3) \
    .nonce(4) \
    .method("transfer")\
    .params(params)\
    .build()

tx_dict = SignedTransaction.to_dict(call_transaction)

signed_transaction_dict = SignedTransaction(call_transaction, wallet1)
tx_hash = icon_service.send_transaction(signed_transaction_dict)
print("transaction result hash: ", tx_hash)

params = {
    "_owner": wallet2.get_address()
}

test_call = CallBuilder()\
    .from_(wallet1.get_address())\
    .to(score_address)\
    .method("balanceOf")\
    .params(params)\
    .build()

result = icon_service.call(test_call)
print("balance: ", convert_hex_str_to_int(result))






