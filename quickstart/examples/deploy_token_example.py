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
from time import sleep
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.builder.transaction_builder import DeployTransactionBuilder, CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from quickstart.examples.test.constant import (
    TEST_HTTP_ENDPOINT_URI_V3,
    TEST_PRIVATE_KEY,
    SCORE_INSTALL_ADDRESS,
    GOVERNANCE_ADDRESS
)
current_dir_path = path.abspath(path.dirname(__file__))
score_path_standard_token = path.join(current_dir_path, 'sample_data/standard_token.zip')
score_path_sample_token = path.join(current_dir_path, 'sample_data/sample_token.zip')

score_paths = [score_path_sample_token, score_path_standard_token]

for score_path in score_paths:
    # Generate deploy data content by reading the zip file data and returning bytes of the file
    install_content_bytes = gen_deploy_data_content(score_path)
    # Loads a wallet from a key store file
    wallet1 = KeyWallet.load(TEST_PRIVATE_KEY)
    print("[wallet1] address: ", wallet1.get_address(), " private key: ", wallet1.get_private_key())

    # Test install SCORE : Checks if making an instance of deploy transaction correctly
    # param = {
    #     "initialSupply": 2000
    # }

    deploy_transaction = DeployTransactionBuilder()\
        .from_(wallet1.get_address())\
        .to(SCORE_INSTALL_ADDRESS) \
        .step_limit(2013265920)\
        .nid(3)\
        .nonce(3)\
        .content_type("application/zip")\
        .content(install_content_bytes)\
        .params('')\
        .version(3)\
        .build()

    signed_transaction_dict = SignedTransaction(deploy_transaction, wallet1)

    icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))

    tx_hash = icon_service.send_transaction(signed_transaction_dict)
    print("txHash: ", tx_hash)

    sleep(1)
    tx_result = icon_service.get_transaction_result(tx_hash)
    print("transaction status(1:success, 0:failure): ", tx_result["status"])
    print("score address: ", tx_result["scoreAddress"])
    print("waiting a second for accepting score...\n")

    # Test install SCORE : Sends a call transaction calling a method `acceptScore` to make the SCORE active
    params = {"txHash": tx_hash}
    call_transaction = CallTransactionBuilder()\
        .from_(wallet1.get_address())\
        .to(GOVERNANCE_ADDRESS) \
        .step_limit(2013265920)\
        .nid(3) \
        .nonce(4) \
        .method("acceptScore")\
        .params(params)\
        .build()

    tx_dict = SignedTransaction.to_dict(call_transaction)

    signed_transaction_dict = SignedTransaction(call_transaction, wallet1)
    tx_hash = icon_service.send_transaction(signed_transaction_dict)
    print("transaction result hash: ", tx_hash, '\n')


