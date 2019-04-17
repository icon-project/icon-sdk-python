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

from unittest import TestCase

from iconsdk.utils.hexadecimal import (
    is_lowercase_hex_string,
    add_0x_prefix,
    add_cx_prefix,
    is_0x_prefixed,
    remove_0x_prefix
)


class TestHexadecimal(TestCase):
    """Unit tests for functions of hexadecimal module"""

    def test_is_lowercase_hex_string(self):
        """Unit test for functional test for the function `is_lowercase_hex_string`.
        """
        valid_value1 = "test".encode().hex()
        valid_value2 = "123".encode().hex()
        is_lowercase_hex_string(valid_value1)
        is_lowercase_hex_string(valid_value2)

        invalid_value1 = "Abcd"
        invalid_value2 = 1234
        invalid_value3 = "123aAc"
        invalid_value4 = "test".encode()
        self.assertFalse(is_lowercase_hex_string(invalid_value1))
        self.assertFalse(is_lowercase_hex_string(invalid_value2))
        self.assertFalse(is_lowercase_hex_string(invalid_value3))
        self.assertFalse(is_lowercase_hex_string(invalid_value4))

    def test_is_hex_string_prefixed_with_0x(self):
        """Unit test for checking whether hex string with 0x or not.
        """

        def is_hex_string_prefixed_with_0x(value: str):
            if is_0x_prefixed(value) and is_lowercase_hex_string(remove_0x_prefix(value)):
                return True
            else:
                return False

        # 0x74657374
        valid_value1 = add_0x_prefix("test".encode().hex())
        self.assertTrue(is_hex_string_prefixed_with_0x(valid_value1))

        # 74657374
        invalid_value1 = remove_0x_prefix(valid_value1)
        self.assertFalse(is_hex_string_prefixed_with_0x(invalid_value1))
        self.assertFalse(is_hex_string_prefixed_with_0x(add_cx_prefix(invalid_value1)))

        invalid_value2 = "Abcd"
        self.assertFalse(is_hex_string_prefixed_with_0x(invalid_value2))
        self.assertFalse(is_hex_string_prefixed_with_0x(add_0x_prefix(invalid_value2)))

        invalid_value3 = "123aAc"
        self.assertFalse(is_hex_string_prefixed_with_0x(invalid_value3))
        self.assertFalse(is_hex_string_prefixed_with_0x(add_0x_prefix(invalid_value3)))


