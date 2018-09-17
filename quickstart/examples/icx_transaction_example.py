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
from time import sleep, time
from pprint import pprint
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import TransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.exception import JSONRPCException
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.builder.call_builder import CallBuilder
from quickstart.examples.test.constant import TEST_HTTP_ENDPOINT_URI_V3, TEST_PRIVATE_KEY, GOVERNANCE_ADDRESS
from quickstart.examples.util.repeater import retry


# Loads a wallet from a key store file
# Wallet for sending ICX
wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)
print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

# Generates a wallet
# Wallet for receiving ICX
wallet2 = KeyWallet.create()
print("[wallet2] address: ", wallet2.get_address(), " private key: ", wallet2.get_private_key())

icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))


# Returns a step cost. You can use it for getting the recommended value of 'step limit'.
def get_default_step_cost():
    _call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getStepCosts")\
        .build()
    _result = icon_service.call(_call)
    default_step_cost = convert_hex_str_to_int(_result["default"])*2
    return default_step_cost


# Generates an instance of transaction for sending icx.
# nid(network id); 1:mainnet, 2~:etc
transaction = TransactionBuilder()\
    .from_(wallet1.get_address())\
    .to(wallet2.get_address())\
    .value(10000)\
    .step_limit(get_default_step_cost()) \
    .nid(3) \
    .nonce(2) \
    .version(3) \
    .timestamp(int(time() * 10 ** 6))\
    .build()

# Returns the signed transaction object having a signature
signed_transaction = SignedTransaction(transaction, wallet1)

# Reads params to transfer to nodes
print("\nparams: ")
pprint(signed_transaction.signed_transaction_dict)

# Sends the transaction
tx_hash = icon_service.send_transaction(signed_transaction)
print("txHash: ", tx_hash)


@retry(JSONRPCException, tries=10, delay=1, back_off=2)
def get_tx_result():
    # Returns the result of a transaction by transaction hash
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("\ntransaction status(1:success, 0:failure): ", tx_result["status"])

    # Gets balance
    balance = icon_service.get_balance(wallet2.get_address())
    print("balance: ", balance, "\n")


get_tx_result()

