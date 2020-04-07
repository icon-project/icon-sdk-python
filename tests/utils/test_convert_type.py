# -*- coding: utf-8 -*-
# Copyright 2019 ICON Foundation
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

from iconsdk.utils.convert_type import convert_int_to_hex_str, convert_hex_str_to_bytes


class TestConvertType(TestCase):
    """Unit tests for functions of convert type module"""

    def test_convert_negative_value_to_hex_str(self):
        """
        Given: Input data is negative.
        When : Converts negative value into hex string.
        Then : Gets return value correctly.
        """
        negative_value = -1
        self.assertEqual(convert_int_to_hex_str(negative_value), '-0x1')

    def test_convert_positive_value_to_hex_str(self):
        """
        Given: Input data is positive.
        When : Converts positive value into hex string.
        Then : Gets return value correctly.
        """
        positive_value = 1
        self.assertEqual(convert_int_to_hex_str(positive_value), '0x1')

    def test_convert_zero_value_to_hex_str(self):
        """
        Given: Input data is zero.
        When : Converts zero value into hex string.
        Then : Gets return value correctly.
        """
        zero_value = 0
        self.assertEqual(convert_int_to_hex_str(zero_value), '0x0')

    def test_convert_hex_str_to_bytes(self):
        """
        Given: Input data is hex str.
        When : Converts hex string to bytes.
        THen : Gets return value correctly.
        """
        hex_str = "0x0000"
        self.assertEqual(convert_hex_str_to_bytes(hex_str), b'\x00\x00')
