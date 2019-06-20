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

from time import sleep

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import DeployTransactionBuilder, CallTransactionBuilder, DepositTransaction, \
    DepositTransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_deploy_transaction, is_T_HASH, is_call_transaction
from tests.api_send.test_send_super import TestSendSuper


class TestSendDeploy(TestSendSuper):

    def test_deploy_integrate(self):
        """
        Integrate-test for deploying SCORE

        1. Installs a SCORE named SampleToken.
        2. Checks if making an instance of installing SCORE transaction correctly.
        *** It needs about 1 sec to build consensus.
        3. Sends a call Transaction which calls a method `acceptScore` to make the new SCORE active
        4. Updates the SCORE having added methods
        5. Checks if making an instance of updating SCORE transaction correctly.
        *** It needs about 1 sec to build consensus.
        6. Sends a call transaction which calls a method `acceptScore` to make the updated SCORE active
        7. Calls a querying method `hello` of the updated SCORE
        8. Calls a querying method `total_supply` of the updated SCORE
        9. Calls a invoking method `transfer` of the updated SCORE
        """
        # Test install SCORE : Checks if making an instance of deploy transaction correctly
        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # Test install SCORE : Sends transaction which makes the SCORE install correctly
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        result_install = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result_install))

        # Test install SCORE : Sends a call transaction calling a method `acceptScore` to make the SCORE active
        params = {"txHash": result_install}
        call_transaction = CallTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_governance"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .method("acceptScore") \
            .params(params) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(call_transaction)
        self.assertTrue(is_call_transaction(tx_dict))

        signed_transaction_dict = SignedTransaction(call_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # Test update SCORE : Checks if making an instance of deploy transaction correctly
        sleep(2)
        installed_score_address = self.icon_service.get_transaction_result(result_install)["scoreAddress"]
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(installed_score_address) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_update"]) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # Test update SCORE : Sends transaction which makes the SCORE update correctly
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        result_update = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result_update))

        # Test update SCORE : Sends a call transaction calling a method `acceptScore` to make the SCORE active
        params = {"txHash": result_update}

        call_transaction = CallTransactionBuilder().from_(self.setting["from"]).to(self.setting["to_governance"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).method("acceptScore").params(
            params).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(call_transaction)
        self.assertTrue(is_call_transaction(tx_dict))

        signed_transaction_dict = SignedTransaction(call_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # Test update SCORE : Calls a method `hello` of the updated SCORE
        sleep(2)
        call_transaction = CallBuilder().from_(self.setting["from"]).to(installed_score_address) \
            .method("hello").build()
        result = self.icon_service.call(call_transaction)
        self.assertEqual(result, "Hello")

        # Test update SCORE : Calls a method `total_supply` of the updated SCORE
        call_transaction = CallBuilder().from_(self.setting["from"]).to(installed_score_address) \
            .method("total_supply").build()
        result = self.icon_service.call(call_transaction)
        self.assertEqual(result, "0x0")

        # Test call a invoking method of SCORE
        value = "0x1"
        params = {
            "addr_to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
            "value": value
        }
        call_transaction = CallTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(installed_score_address) \
            .method("transfer") \
            .params(params) \
            .nid(self.setting["nid"]) \
            .step_limit(self.setting["step_limit"]) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(call_transaction)
        self.assertTrue(is_call_transaction(tx_dict))

        signed_transaction_dict = SignedTransaction(call_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_installing_score_validation(self):
        # Test install SCORE : When not having an optional property, nonce
        deploy_transaction = DeployTransactionBuilder().from_(self.setting["from"]).to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .build()
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # Test install SCORE : When not having a required property - contentType
        deploy_transaction_builder = DeployTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .content(self.setting["content_install"])
        self.assertRaises(DataTypeException, deploy_transaction_builder.build)

        # Test install SCORE : When data type of the address is wrong
        wrong_address = "hx4873b94352c8c1f3b2f09aaeccea31ce9e90"
        deploy_transaction = DeployTransactionBuilder().from_(wrong_address).to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .build()
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # Test install SCORE : When a sending address is wrong - not the wallet's address
        wrong_address = "hx5bfdb090f43a808005ffc27c25b213145e80b7cd"
        deploy_transaction = DeployTransactionBuilder().from_(wrong_address).to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .build()
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

    def test_deposit_add_and_withdraw(self):
        # Test install SCORE : Checks if making an instance of deploy transaction correctly
        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # Test install SCORE : Sends transaction which makes the SCORE install correctly
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        result_install = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result_install))

        sleep(2)
        installed_score_address = self.icon_service.get_transaction_result(result_install)["scoreAddress"]

        _DEPOSIT_AMOUNT = 5000 * (10 ** 18)
        deposit_transaction_of_add_0: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(installed_score_address) \
            .value(_DEPOSIT_AMOUNT) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("add") \
            .build()

        # Checks if sending transaction correctly
        signed_transaction_dict = SignedTransaction(deposit_transaction_of_add_0, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        sleep(2)
        self.assertEqual(self.icon_service.get_transaction_result(result)["status"], 1)

        # transaction instance for withdraw action
        deposit_transaction_of_withdraw: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(installed_score_address) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .id(result) \
            .action("withdraw") \
            .build()

        signed_transaction_dict = SignedTransaction(deposit_transaction_of_withdraw, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        sleep(2)
        self.assertEqual(self.icon_service.get_transaction_result(result)["status"], 1)
