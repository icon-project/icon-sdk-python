# -*- coding: utf-8 -*-
# Copyright 2017-2018 theloop Inc.
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

import unittest
from IconService.builder.tx_builder import IcxTransactionBuilder, CallTransactionBuilder,\
    DeployTransactionBuilder, MessageTransactionBuilder


class TestTransactionBuilder(unittest.TestCase):

    general_tx_properties = ["from_", "to", "value", "step_limit", "nonce"]

    def test_make_icx_transaction(self):
        """Testing for making a icx transaction successfully"""

        icx_tx = IcxTransactionBuilder()\
            .from_("FROM_")\
            .to("TO")\
            .value("VALUE")\
            .step_limit("STEP_LIMIT")\
            .nonce("NONCE")\
            .build()

        # checks all of property is collect.
        for idx, property in enumerate(self.general_tx_properties):
            self.assertEqual(getattr(icx_tx, property), property.upper())

    def test_make_call_transaction(self):
        """Testing for making a call transaction successfully"""
        call_tx_properties = ["method", "params"]
        call_tx = CallTransactionBuilder() \
            .from_("FROM_") \
            .to("TO") \
            .value("VALUE") \
            .step_limit("STEP_LIMIT") \
            .nonce("NONCE") \
            .method("METHOD") \
            .params("PARAMS") \
            .build()

        for idx, property in enumerate(self.general_tx_properties + call_tx_properties):
            self.assertEqual(getattr(call_tx, property), property.upper())

    def test_make_deploy_transaction(self):
        """Testing for making a deploy transaction successfully"""
        deploy_tx_properties = ["content_type", "content", "params"]
        deploy_tx = DeployTransactionBuilder() \
            .from_("FROM_") \
            .to("TO") \
            .value("VALUE") \
            .step_limit("STEP_LIMIT") \
            .nonce("NONCE") \
            .content_type("CONTENT_TYPE") \
            .content("CONTENT") \
            .params("PARAMS") \
            .build()

        for idx, property in enumerate(self.general_tx_properties + deploy_tx_properties):
            self.assertEqual(getattr(deploy_tx, property), property.upper())

    def test_make_message_transaction(self):
        """Testing for making a message transaction successfully"""
        message_tx_properties = ["data"]
        message_tx = MessageTransactionBuilder() \
            .from_("FROM_") \
            .to("TO") \
            .value("VALUE") \
            .step_limit("STEP_LIMIT") \
            .nonce("NONCE") \
            .data("DATA") \
            .build()

        for idx, property in enumerate(self.general_tx_properties + message_tx_properties):
            self.assertEqual(getattr(message_tx, property), property.upper())

    def test_make_message_tx_builder_changed(self):
        """Testing for making a message transaction builder changed, it should not work."""
        message_tx = MessageTransactionBuilder() \
            .from_("FROM_") \
            .to("TO") \
            .value("VALUE") \
            .step_limit("STEP_LIMIT") \
            .nonce("NONCE") \
            .data("DATA") \
            .build()

        def test_set_message_tx_builder():
            message_tx.data = "NEW_DATA"

        self.assertRaises(AttributeError, test_set_message_tx_builder)


