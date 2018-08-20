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

from tests.api_send.test_send_super import TestSendSuper

from IconService.builder.transaction_builder import MessageTransactionBuilder
from IconService.signed_transaction import SignedTransaction
from IconService.utils.validation import is_message_transaction, is_T_HASH
from IconService.exception import JSONRPCException


class TestSendMessage(TestSendSuper):

    def test_send_message(self):

        # Checks if making an instance of message transaction correctly
        message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]).data(self.setting["data"]).build()
        tx_dict = SignedTransaction.to_dict(message_transaction)
        self.assertTrue(is_message_transaction(tx_dict))

        # Checks if sending transaction correctly
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When having an optional property, nonce
        message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When address is wrong
        message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"][2:]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When not having a required property, nid
        message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"][2:]) \
            .step_limit(self.setting["step_limit"]).data(self.setting["data"]).build()
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)

        # When a sending address is wrong - not the wallet's address
        message_transaction = MessageTransactionBuilder().from_(self.setting["to"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        self.assertRaises(JSONRPCException, self.icon_service.send_transaction, signed_transaction_dict)
