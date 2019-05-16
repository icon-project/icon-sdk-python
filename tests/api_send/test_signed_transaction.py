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

from unittest import main

from iconsdk.builder.transaction_builder import TransactionBuilder, MessageTransactionBuilder, \
    CallTransactionBuilder, DeployTransactionBuilder
from iconsdk.exception import DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_icx_transaction, is_call_transaction, is_message_transaction, \
    is_deploy_transaction, is_T_HASH
from tests.api_send.test_send_super import TestSendSuper


class TestSignedTransaction(TestSendSuper):

    def test_to_dict(self):
        # Transfer
        # When having an optional property, nonce
        icx_transaction = TransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))
        # When not having an optional property, nonce
        icx_transaction = TransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(icx_transaction)
        self.assertTrue(is_icx_transaction(tx_dict))
        # When not having an required property, value
        icx_transaction = TransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(icx_transaction)
        self.assertFalse(is_icx_transaction(tx_dict))

        # Update SCORE
        deploy_transaction = DeployTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).content_type(self.setting["content_type"]) \
            .content(self.setting["content_update"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # Install SCORE
        deploy_transaction = DeployTransactionBuilder().from_(self.setting["from"]).to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .params(self.setting["params_install"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(deploy_transaction)
        self.assertTrue(is_deploy_transaction(tx_dict))

        # SCORE method call
        call_transaction = CallTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .method(self.setting["method"]).params(self.setting["params_call"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(call_transaction)
        self.assertTrue(is_call_transaction(tx_dict))

        # Message send
        msg_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(msg_transaction)
        self.assertTrue(is_message_transaction(tx_dict))

    def test_signed_transaction_transfer(self):
        icx_transaction = TransactionBuilder().from_(self.wallet.get_address()).to(self.setting["to"]) \
            .value(self.setting["value"]).step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()
        signed_transaction_dict = SignedTransaction(icx_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_signed_transaction_with_icx_transaction_without_step_limit(self):
        icx_transaction_without_step_limit = TransactionBuilder().from_(self.wallet.get_address()).to(
            self.setting["to"]) \
            .value(self.setting["value"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).build()

        # fail without step limit
        self.assertRaises(DataTypeException, SignedTransaction, icx_transaction_without_step_limit, self.wallet)

        # success with param of step limit
        signed_transaction_dict = SignedTransaction(icx_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_signed_transaction_with_deploy_transaction_without_step_limit(self):
        deploy_transaction_without_step_limit = DeployTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to_install"]) \
            .nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]).content(self.setting["content_install"]) \
            .params(self.setting["params_install"]).build()

        # fail without step limit
        self.assertRaises(DataTypeException, SignedTransaction, deploy_transaction_without_step_limit, self.wallet)

        # success with param of step limit
        signed_transaction_dict = SignedTransaction(deploy_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_signed_transaction_with_call_transaction_without_step_limit(self):
        call_transaction_without_step_limit = CallTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to"]) \
            .nid(self.setting["nid"]).nonce(self.setting["nonce"]) \
            .method(self.setting["method"]).params(self.setting["params_call"]).build()

        # fail without step limit
        self.assertRaises(DataTypeException, SignedTransaction, call_transaction_without_step_limit, self.wallet)

        # success with param of step limit
        signed_transaction_dict = SignedTransaction(call_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_signed_transaction_with_message_transaction_without_step_limit(self):
        msg_transaction_without_step_limit = MessageTransactionBuilder().from_(self.setting["from"]).to(
            self.setting["to"]) \
            .nid(self.setting["nid"]).data(self.setting["data"]).build()

        # fail without step limit
        self.assertRaises(DataTypeException, SignedTransaction, msg_transaction_without_step_limit, self.wallet)

        # success with param of step limit
        signed_transaction_dict = SignedTransaction(msg_transaction_without_step_limit, self.wallet,
                                                    self.setting["step_limit"])
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))


if __name__ == "__main__":
    main()
