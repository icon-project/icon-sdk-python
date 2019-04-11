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

from unittest import TestCase, main
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder,
    DeployTransactionBuilder
)
from iconsdk.utils import get_timestamp
from iconsdk.wallet.wallet import KeyWallet
from tests.example_config import TEST_PRIVATE_KEY
from iconsdk.utils.validation import has_keys, is_0x_prefixed
from copy import deepcopy
from iconsdk.exception import DataTypeException


class TestTransactionBuilder(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Sets needed data like an instance of a wallet and iconsdk
        and default values used to make 4 types of transactions. (transfer, call, deploy, message)
        """
        cls.wallet = KeyWallet.load(TEST_PRIVATE_KEY)

        install_content_bytes = b'install_test'
        update_content_bytes = b'update_test'

        cls.transaction_as_setting = {
            "from_": cls.wallet.get_address(),
            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
            "to_governance": "cx0000000000000000000000000000000000000001",
            "step_limit": 4000000000,
            "nid": 3,
            "nonce": 3,
            # It is used to send icx(transfer) only.
            "value": 1000000000000000000,
            # It is used to send call only.
            "method": "transfer",
            "params_call": {
                "to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
                "value": "0x1"
            },
            # It is used to send SCORE install(deploy).
            # If SCORE's address is as follows, it means install SCORE.
            "to_install": "cx0000000000000000000000000000000000000000",
            "content_type": "application/zip",
            # Data type of content should be bytes.
            "content_install": install_content_bytes,
            "content_update": update_content_bytes,
            # It is used to deploy only.(install)
            "params_install": {
                "init_supply": 10000
            },
            # It is used to send message only.
            "data": "0x" + "test".encode().hex(),
            "version": 3,
            "timestamp": get_timestamp()
        }

    def _is_basic_transaction(self, params: dict) -> bool:
        """
        Checks `Transaction` in dict has right format.
        Every types of `Transaction` like icx transaction, deploy transaction, call transaction and message transaction
        is checked by this method.
        """
        inner_key_of_params = ['version', 'from_', 'to', 'step_limit', 'timestamp', 'nid', 'nonce', 'value']
        return has_keys(params, inner_key_of_params)

    def _is_icx_transaction(self, params: dict) -> bool:
        """Checks `Transaction` in dict for transfer icx has right format."""
        return self._is_basic_transaction(params)

    def _is_deploy_transaction(self, params: dict) -> bool:
        """Checks `DeployTransaction` in dict has right format."""
        inner_key_of_params = ['params', 'content_type', 'content', 'data_type']

        return self._is_basic_transaction(params) \
               and has_keys(params, inner_key_of_params) \
               and params['data_type'] == 'deploy' \
               and isinstance(params['content'], bytes) \
               and not params['value']

    def _is_call_transaction(self, params: dict) -> bool:
        """Checks `CallTransaction` in dict has right format."""
        inner_key_of_params = ['data_type', 'params', 'method']
        return self._is_basic_transaction(params) \
               and has_keys(params, inner_key_of_params) \
               and params["data_type"] == "call"

    def _is_message_transaction(self, params: dict) -> bool:
        """Checks `MessageTransaction` in dict has right format."""
        inner_key_of_params = ['data_type', 'data']
        return self._is_basic_transaction(params) \
               and has_keys(params, inner_key_of_params) \
               and isinstance(params["data"], str) \
               and is_0x_prefixed(params["data"]) \
               and params["data_type"] == "message"

    def test_transaction_builder_from_dict(self):
        """Test for all kind of transaction builders to support for making each transaction from dict"""

        # case 0 for icx transaction : successful case with every fields of basic transaction
        input_transaction_as_dict = {
            "from_": self.transaction_as_setting["from_"],
            "to": self.transaction_as_setting["to"],
            "value": self.transaction_as_setting["value"],
            "step_limit": self.transaction_as_setting["step_limit"],
            "nid": self.transaction_as_setting["nid"],
            "nonce": self.transaction_as_setting["nonce"],
            "version": self.transaction_as_setting["version"],
            "timestamp": self.transaction_as_setting["timestamp"]
        }
        transaction = TransactionBuilder.from_dict(input_transaction_as_dict).build()
        transaction_as_dict = transaction.to_dict()
        self.assertTrue(self._is_icx_transaction(transaction_as_dict))
        self.assertEqual(input_transaction_as_dict, transaction_as_dict)

        # case 1 for icx transaction : successful case without the optional field same as nid
        input_transaction_as_dict2 = deepcopy(input_transaction_as_dict)
        del input_transaction_as_dict2["nid"]
        transaction = TransactionBuilder.from_dict(input_transaction_as_dict2).build()
        transaction_as_dict = transaction.to_dict()
        self.assertTrue(self._is_icx_transaction(transaction_as_dict))
        self.assertEqual(None, transaction_as_dict["nid"])

        # case 2 for icx transaction : failed case without the required field same as step_limit
        input_transaction_as_dict3 = deepcopy(input_transaction_as_dict)
        del input_transaction_as_dict3["step_limit"]
        self.assertRaises(DataTypeException, TransactionBuilder.from_dict, input_transaction_as_dict3)

        # case 0 for call transaction : successful case with every fields of call transaction
        input_call_transaction_as_dict = deepcopy(input_transaction_as_dict)
        tmp_other_fields = {"method": self.transaction_as_setting["method"], "params": {"key1": "value1"}}
        input_call_transaction_as_dict.update(tmp_other_fields)
        call_transaction = CallTransactionBuilder.from_dict(input_call_transaction_as_dict).build()
        call_transaction_as_dict = call_transaction.to_dict()
        self.assertTrue(self._is_call_transaction(call_transaction_as_dict))

        # case 1 for call transaction : successful case without the optional field same as params
        input_call_transaction_as_dict2 = deepcopy(input_call_transaction_as_dict)
        del input_call_transaction_as_dict2["params"]
        call_transaction = CallTransactionBuilder.from_dict(input_call_transaction_as_dict2).build()
        call_transaction_as_dict = call_transaction.to_dict()
        self.assertTrue(
            isinstance(CallTransactionBuilder.from_dict(input_call_transaction_as_dict2), CallTransactionBuilder))
        self.assertTrue(self._is_call_transaction(call_transaction_as_dict))

        # case 2 for call transaction : failed case without the required field same as method
        input_call_transaction_as_dict3 = deepcopy(input_call_transaction_as_dict)
        del input_call_transaction_as_dict3["method"]
        self.assertRaises(DataTypeException, CallTransactionBuilder.from_dict, input_call_transaction_as_dict3)

        # case 0 for message transaction : failed case without the required field same as data
        input_message_transaction_as_dict = deepcopy(input_transaction_as_dict)
        self.assertRaises(DataTypeException, MessageTransactionBuilder.from_dict, input_message_transaction_as_dict)

        # case 1 for message transaction : successful case with every fields of message transaction
        tmp_other_fields = {'data': self.transaction_as_setting['data']}
        input_message_transaction_as_dict.update(tmp_other_fields)
        message_transaction = MessageTransactionBuilder.from_dict(input_message_transaction_as_dict).build()
        message_transaction_as_dict = message_transaction.to_dict()
        self.assertTrue(
            isinstance(MessageTransactionBuilder.from_dict(input_message_transaction_as_dict), MessageTransactionBuilder))
        self.assertTrue(self._is_message_transaction(message_transaction_as_dict))

        # case 0 for deploy transaction : successful case with every fields of deploy transaction
        input_deploy_transaction_as_dict = deepcopy(input_transaction_as_dict)
        tmp_other_fields = {
            'content': self.transaction_as_setting['content_install'],
            'content_type': self.transaction_as_setting['content_type'],
            'params': {'key1': 'value1'}}
        input_deploy_transaction_as_dict.update(tmp_other_fields)
        deploy_transaction = DeployTransactionBuilder.from_dict(input_deploy_transaction_as_dict).build()
        deploy_transaction_as_dict = deploy_transaction.to_dict()
        self.assertTrue(
            isinstance(DeployTransactionBuilder.from_dict(input_deploy_transaction_as_dict), DeployTransactionBuilder))
        self.assertTrue(self._is_deploy_transaction(deploy_transaction_as_dict))


if __name__ == "__main__":
    main()
