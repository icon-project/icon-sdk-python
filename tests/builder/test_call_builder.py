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

from iconsdk.builder.call_builder import CallBuilder


class TestCallBuilder(TestCase):

    def test_make_call_builder(self):
        """Testing for making a couple of call builders successfully"""

        call_1 = CallBuilder()          \
            .from_("1_FROM")            \
            .to("1_TO")                 \
            .method("1_METHOD")         \
            .params({"test": 123})      \
            .build()

        call_2 = CallBuilder().from_("2_FROM").to("2_TO").method("2_METHOD").params({"test": 123}).build()

        properties = ["from_", "to", "method", "params"]
        values_call_1 = ["1_FROM", "1_TO", "1_METHOD", {'test': '0x7b'}]
        values_call_2 = ["2_FROM", "2_TO", "2_METHOD", {'test': '0x7b'}]

        # Checks all of property is collect.
        for idx, property in enumerate(properties):
            self.assertEqual(getattr(call_1, property), values_call_1[idx])
            self.assertEqual(getattr(call_2, property), values_call_2[idx])

    def test_make_call_builder_changed(self):
        """Testing for making a call builder changed, it should not work."""

        call_1 = CallBuilder()       \
            .from_("1_FROM")         \
            .to("1_TO")              \
            .method("1_METHOD")      \
            .params("1_PARAMS")      \
            .build()

        def test_set_call_builder():
            call_1.from_ = "1_NEW_PROM"

        self.assertRaises(AttributeError, test_set_call_builder)


if __name__ == "__main__":
    main()
