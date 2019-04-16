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
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from tests.example_config import TEST_HTTP_ENDPOINT_URI_V3


class TestCall(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.wallet = KeyWallet.create()
        cls.address = cls.wallet.get_address()
        cls.to = "cx0000000000000000000000000000000000000001"
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))

    def test_call(self):
        test_call = CallBuilder().from_(self.address).to(self.to).method("getStepCosts").params("").build()
        result = self.icon_service.call(test_call)
        self.assertTrue(result)

        test_call = CallBuilder().from_(self.address).to(self.to).method("getStepCosts").build()
        result = self.icon_service.call(test_call)
        self.assertTrue(result)


if __name__ == "__main__":
    main()
