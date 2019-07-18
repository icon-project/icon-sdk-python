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

import os

from time import sleep
from unittest import main

from iconsdk.builder.transaction_builder import (TransactionBuilder, CallTransactionBuilder,
                                                 DeployTransactionBuilder, MessageTransactionBuilder,
                                                 DepositTransaction, DepositTransactionBuilder)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.hexadecimal import remove_0x_prefix, add_0x_prefix
from iconsdk.utils.validation import is_block, is_T_HASH, is_score_apis, is_transaction, is_transaction_result
from tests.api_full_response.example_response import result_error_v3, result_success_v3
from tests.api_send.test_send_super import TestSendSuper


class TestCheckFullResponse(TestSendSuper):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        result = cls.icon_service.get_block("latest")
        cls.from_ = cls.setting['from']

        # When having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(cls.setting["from"]) \
            .to(cls.setting["to"]) \
            .value(cls.setting["value"]) \
            .step_limit(cls.setting["step_limit"]) \
            .nid(3) \
            .nonce(cls.setting["nonce"]) \
            .version(3) \
            .build()

        signed_transaction_dict = SignedTransaction(icx_transaction, cls.wallet)
        tx_result = cls.icon_service.send_transaction(signed_transaction_dict)
        sleep(2)
        cls.tx_hash = tx_result
        cls.tx_hash_invalid = "0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238"
        cls.governance_address = "cx0000000000000000000000000000000000000001"
        cls.valid_hash = add_0x_prefix(result["block_hash"])

    def test_get_balance_full_response(self):
        # get_balance with full_response
        result_dict = self.icon_service.get_balance(self.from_, True)
        result_keys = result_dict.keys()
        result_contents = result_dict['result']
        self.assertEqual(result_success_v3.keys(), result_keys)
        self.assertIsInstance(int(result_contents, 16), int)

    def test_get_block_by_hash_full_response(self):
        # used valid hash and got and valid block
        result_block_dict = self.icon_service.get_block(self.valid_hash, True)
        result_block_keys = result_block_dict.keys()
        result_block_contents = result_block_dict['result']
        self.assertEqual(result_success_v3.keys(), result_block_keys)
        self.assertTrue(is_block(result_block_contents))

        # used invalid hash and got and invalid block
        invalid_hash = "0x033f8d96045eb8301fd17cf078c28ae58a3ba329f6ada5cf128ee56dc2af26f7"
        result_block_dict = self.icon_service.get_block(invalid_hash, True)
        result_block_keys = result_block_dict.keys()
        self.assertEqual(result_error_v3.keys(), result_block_keys)

    def test_get_block_by_height_full_response(self):
        # used 0(genesis block) and got valid block
        result_block_dict = self.icon_service.get_block(0, True)
        result_block_keys = result_block_dict.keys()
        result_block_contents = result_block_dict['result']
        self.assertEqual(result_success_v3.keys(), result_block_keys)
        self.assertTrue(is_block(result_block_contents))

        block = self.icon_service.get_block("latest")
        height_of_latest_block = block['height']

        # used invalid height and got invalid block
        result_block_dict = self.icon_service.get_block(height_of_latest_block + 1, True)
        result_block_keys = result_block_dict.keys()
        self.assertEqual(result_error_v3.keys(), result_block_keys)

    def test_get_last_block_full_response(self):
        result_block_dict = self.icon_service.get_block("latest", True)
        result_block_keys = result_block_dict.keys()

        result_block_contents = result_block_dict['result']

        self.assertEqual(result_success_v3.keys(), result_block_keys)
        self.assertTrue(is_block(result_block_contents))

    def test_get_score_api_full_response(self):
        # when getting score apis successfully
        full_response_result = self.icon_service.get_score_api(self.governance_address, True)
        self.assertEqual(result_success_v3.keys(), full_response_result.keys())
        self.assertTrue(is_score_apis(full_response_result['result']))

        # when the address is not score id
        full_response_result = self.icon_service.get_score_api("cxb0776ee37f5b45bfaea8cff1d8232fbb6122ec32", True)
        full_response_keys = full_response_result.keys()
        self.assertEqual(result_error_v3.keys(), full_response_keys)

    def test_get_total_supply_full_response(self):
        result_block_dict = self.icon_service.get_total_supply(True)
        result_block_keys = result_block_dict.keys()

        total_supply = self.icon_service.get_total_supply()
        result_block_contents = result_block_dict['result']
        compared_total_supply = int(remove_0x_prefix(result_block_contents), 16)

        self.assertEqual(result_success_v3.keys(), result_block_keys)
        self.assertEqual(total_supply, compared_total_supply)

    def test_transaction_by_hash_full_response(self):
        # used valid hash and got a valid transaction
        result_transaction_dict = self.icon_service.get_transaction(self.tx_hash, True)
        result_transaction_keys = result_transaction_dict.keys()
        result_transaction_contents = result_transaction_dict['result']
        self.assertEqual(result_success_v3.keys(), result_transaction_keys)
        self.assertTrue(is_transaction(result_transaction_contents))

        # used invalid hash and got an invalid transaction
        result_transaction_dict = self.icon_service.get_transaction(self.tx_hash_invalid, True)
        result_transaction_keys = result_transaction_dict.keys()
        self.assertEqual(result_error_v3.keys(), result_transaction_keys)

    def test_get_transaction_result_full_response(self):
        # used valid hash and got a valid transaction result
        result_block_dict = self.icon_service.get_transaction_result(self.tx_hash, True)
        result_block_keys = result_block_dict.keys()
        result_contents = result_block_dict['result']
        self.assertEqual(result_success_v3.keys(), result_block_keys)
        self.assertTrue(is_transaction_result(result_contents))

        # used invalid hash and got an invalid transaction result
        tx_hash_invalid = add_0x_prefix(os.urandom(32).hex())
        result_block_dict = self.icon_service.get_transaction_result(tx_hash_invalid, True)
        result_block_keys = result_block_dict.keys()
        self.assertEqual(result_error_v3.keys(), result_block_keys)

    def test_deposit_full_response(self):
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"

        # deposit add action transaction
        deposit_transaction_without_step_limit: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("add") \
            .build()

        signed_transaction_dict = SignedTransaction(deposit_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        deposit_transaction_without_step_limit: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(wrong_address) \
            .value(self.setting["value"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("add") \
            .build()

        signed_transaction_dict = SignedTransaction(deposit_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_error_v3.keys(), result.keys())

        # deposit withdraw action transaction
        deposit_transaction_without_step_limit: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("withdraw") \
            .id(self.setting["id"]) \
            .build()

        signed_transaction_dict = SignedTransaction(deposit_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        # when transaction failed
        deposit_transaction_without_step_limit: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(wrong_address) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("withdraw") \
            .id(self.setting["id"]) \
            .build()

        signed_transaction_dict = SignedTransaction(deposit_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_error_v3.keys(), result.keys())

    def test_send_message_full_response(self):
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"

        # message transaction
        msg_transaction_without_step_limit = MessageTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to"]) \
            .nid(self.setting["nid"]).data(self.setting["data"]).build()

        signed_transaction_dict = SignedTransaction(msg_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        # when transaction failed
        msg_transaction_without_step_limit = MessageTransactionBuilder().from_(self.setting["from"]).to(
            wrong_address) \
            .nid(self.setting["nid"]).data(self.setting["data"]).build()

        signed_transaction_dict = SignedTransaction(msg_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_error_v3.keys(), result.keys())

    def test_send_transfer_with_full_response(self):
        # When not having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .build()

        # transaction succeed
        signed_transaction = SignedTransaction(icx_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction, True)

        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        # when transaction failed.
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(wrong_address) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .build()
        signed_transaction = SignedTransaction(icx_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction, True)
        self.assertEqual(result_error_v3.keys(), result.keys())

    def test_deploy_transaction_with_full_response(self):
        # deploy transaction
        deploy_transaction = DeployTransactionBuilder().from_(self.setting["from"]).to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .params(self.setting["params_install"]).build()

        # transaction succeed
        signed_transaction = SignedTransaction(deploy_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction, True)

        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        # when transaction failed.
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"
        deploy_transaction = DeployTransactionBuilder().from_(self.setting["from"]).to(wrong_address) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .params(self.setting["params_install"]).build()

        signed_transaction = SignedTransaction(deploy_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction, True)
        self.assertEqual(result_error_v3.keys(), result.keys())

    def test_call_transaction_with_full_response(self):
        # call transaction
        call_transaction_without_step_limit = CallTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to"]) \
            .nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .method(self.setting["method"]).params(self.setting["params_call"]).build()
        signed_transaction_dict = SignedTransaction(call_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)

        self.assertEqual(result_success_v3.keys(), result.keys())
        self.assertTrue(is_T_HASH(result['result']))

        # when transaction failed
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e8"
        call_transaction_without_step_limit = CallTransactionBuilder().from_(self.setting["from"]).to(
            wrong_address) \
            .nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .method(self.setting["method"]).params(self.setting["params_call"]).build()
        signed_transaction_dict = SignedTransaction(call_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict, True)
        self.assertEqual(result_error_v3.keys(), result.keys())


if __name__ == "__main__":
    main()
