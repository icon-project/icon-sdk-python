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
from pprint import pprint

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.exception import JSONRPCException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.wallet.wallet import KeyWallet
from quickstart.examples.test.constant import (
    BASE_DOMAIN_URL_V3_FOR_TEST,
    PRIVATE_KEY_FOR_TEST,
    GOVERNANCE_ADDRESS,
    SCORE_ADDRESS,
    VERSION_FOR_TEST
)
from quickstart.examples.util.repeater import retry


# Returns a step cost. You can use it for getting the recommended value of 'step limit'.
def get_default_step_cost():
    _call = CallBuilder() \
        .from_(wallet1.get_address()) \
        .to(GOVERNANCE_ADDRESS) \
        .method("getStepCosts") \
        .build()
    _result = icon_service.call(_call)
    default_step_cost = convert_hex_str_to_int(_result["default"])
    return default_step_cost


icon_service = IconService(HTTPProvider(BASE_DOMAIN_URL_V3_FOR_TEST, VERSION_FOR_TEST))

wallet1 = KeyWallet.load(PRIVATE_KEY_FOR_TEST)

# Loads a wallet from a key store file.
wallet2 = KeyWallet.load("./test/test_keystore", "abcd1234*")
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

params = {"_to": wallet2.get_address(), "_value": 10}

# Enters transaction information.
call_transaction = CallTransactionBuilder() \
    .from_(wallet1.get_address()) \
    .to(SCORE_ADDRESS) \
    .step_limit(get_default_step_cost() * 2) \
    .nid(3) \
    .nonce(4) \
    .method("transfer") \
    .params(params) \
    .build()

# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(call_transaction, wallet1)

# Reads params to transfer to nodes
print("params:")
pprint(signed_transaction.signed_transaction_dict)

# Sends transaction
tx_hash = icon_service.send_transaction(signed_transaction)
print("txHash: ", tx_hash)


@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx_result():
    # Returns the result of a transaction by transaction hash
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("transaction status(1:success, 0:failure): ", tx_result["status"])


get_tx_result()

params = {
    "_owner": wallet2.get_address()
}

call = CallBuilder() \
    .from_(wallet1.get_address()) \
    .to(SCORE_ADDRESS) \
    .method("balanceOf") \
    .params(params) \
    .build()

result = icon_service.call(call)
print("balance: ", convert_hex_str_to_int(result))
