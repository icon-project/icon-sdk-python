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

from iconsdk.builder.transaction_builder import MessageTransactionBuilder
from iconsdk.exception import JSONRPCException, DataTypeException
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_message_transaction, is_T_HASH
from tests.api_send.test_send_super import TestSendSuper


class TestSendMessage(TestSendSuper):

    def test_send_message(self):
        sleep_time = 2

        # Checks if making an instance of message transaction correctly
        message_transaction = MessageTransactionBuilder()\
            .from_(self.setting["from"])\
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"])\
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"])\
            .data(self.setting["data"]).build()
        tx_dict = SignedTransaction.convert_tx_to_jsonrpc_request(message_transaction)
        self.assertTrue(is_message_transaction(tx_dict))

        # Checks if sending transaction correctly
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When having an optional property, nonce
        sleep(sleep_time)
        message_transaction = MessageTransactionBuilder().from_(self.setting["from"]).to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]).nid(self.setting["nid"]).data(self.setting["data"]).build()
        signed_transaction_dict = SignedTransaction(message_transaction, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

        # When the data is hex string
        sleep(sleep_time)
        tx_result = self.icon_service.get_transaction_result(result)
        tx = self.icon_service.get_transaction(result)

        # Checks the transaction
        self.assertEqual(tx["data"], self.setting["data"])
        block = self.icon_service.get_block(int(tx_result["blockHeight"]))

        # Checks the block's transaction
        self.assertEqual(block["confirmed_transaction_list"][0]["data"], self.setting["data"])

        # When data is not hex string
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data("test")

        # Raise DataTypeException
        self.assertRaises(DataTypeException, message_transaction.build)

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


