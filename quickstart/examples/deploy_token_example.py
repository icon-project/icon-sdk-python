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

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.exception import JSONRPCException
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.convert_type import convert_hex_str_to_int
from iconsdk.wallet.wallet import KeyWallet
from quickstart.examples.test.constant import (
    TEST_HTTP_ENDPOINT_URI_V3,
    TEST_PRIVATE_KEY,
    SCORE_INSTALL_ADDRESS,
    GOVERNANCE_ADDRESS
)
from quickstart.examples.util.repeater import retry

current_dir_path = path.abspath(path.dirname(__file__))
score_path_standard_token = path.join(current_dir_path, 'sample_data/standard_token.zip')
score_path_sample_token = path.join(current_dir_path, 'sample_data/sample_token.zip')
score_paths = [score_path_sample_token, score_path_standard_token]
icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))


# Returns the max step limit
def get_max_step_limit():
    _param = {
        "contextType": "invoke"
    }
    _call = CallBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS)\
        .method("getMaxStepLimit")\
        .params(_param)\
        .build()
    _result = icon_service.call(_call)
    return convert_hex_str_to_int(_result)


for score_path in score_paths:
    # Reads the zip file 'standard_token.zip' and returns bytes of the file
    install_content_bytes = gen_deploy_data_content(score_path)
    # Loads a wallet from a key store file
    wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)
    print("="*100)
    print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

    # Enters transaction information
    deploy_transaction = DeployTransactionBuilder()\
        .from_(wallet1.get_address())\
        .to(SCORE_INSTALL_ADDRESS) \
        .step_limit(get_max_step_limit())\
        .nid(3)\
        .nonce(3)\
        .content_type("application/zip")\
        .content(install_content_bytes)\
        .version(3)\
        .build()

    # Returns the signed transaction object having a signature
    signed_transaction_dict = SignedTransaction(deploy_transaction, wallet1)

    # Sends the transaction
    tx_hash = icon_service.send_transaction(signed_transaction_dict)
    print("txHash: ", tx_hash)

    @retry(JSONRPCException, tries=10, delay=2, back_off=2)
    def get_tx_result():
        # Returns the result of a transaction by transaction hash
        tx_result = icon_service.get_transaction_result(tx_hash)
        print("transaction status(1:success, 0:failure): ", tx_result["status"])
        print("score address: ", tx_result["scoreAddress"])
        print("waiting a second for accepting score...\n")

    get_tx_result()
