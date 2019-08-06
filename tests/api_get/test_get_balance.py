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

from iconsdk.exception import AddressException
from tests.api_send.test_send_super import TestSendSuper


class TestGetBalance(TestSendSuper):

    def test_get_balance_from_wallet(self):
        # case 0: get balance from wallet or score successfully.
        result = self.icon_service.get_balance(self.setting["from"])
        self.assertTrue(isinstance(result, int))
        result = self.icon_service.get_balance(self.setting["to"])
        self.assertTrue(isinstance(result, int))

        # case 1: when a param is wrong.
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["to"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, self.setting["from"][2:])
        self.assertRaises(AddressException, self.icon_service.get_balance, "123")
        self.assertRaises(AddressException, self.icon_service.get_balance, 123)
        # when the address's length is short
        self.assertRaises(AddressException, self.icon_service.get_balance, "cx882efc17c2f50e0d60142b9c0e746cbafb569d")


if __name__ == "__main__":
    main()
