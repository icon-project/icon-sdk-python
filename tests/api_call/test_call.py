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

import json
from unittest import TestCase, main

import requests_mock

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST, VERSION_FOR_TEST


class TestCall(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wallet = KeyWallet.create()
        cls.address = cls.wallet.get_address()
        cls.to = "cx0000000000000000000000000000000000000001"
        cls.icon_service = IconService(HTTPProvider(BASE_DOMAIN_URL_V3_FOR_TEST, VERSION_FOR_TEST))
        cls.ret_json = {
            "jsonrpc": "2.0",
            "result": {
                "default": "0x186a0",
                "contractCall": "0x61a8",
                "contractCreate": "0x3b9aca00",
                "contractUpdate": "0x5f5e1000",
                "contractDestruct": "-0x11170",
                "contractSet": "0x7530",
                "get": "0x0",
                "set": "0x140",
                "replace": "0x50",
                "delete": "-0xf0",
                "input": "0xc8",
                "eventLog": "0x64",
                "apiCall": "0x2710"
            },
            "id": 1234
        }

    def test_call1_default(self):
        # with from
        test_call = CallBuilder().\
            from_(self.address).\
            to(self.to).\
            method("getStepCosts").\
            params({}).\
            build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.to,
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                    "from": self.address
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=self.ret_json)
            result = self.icon_service.call(test_call)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
        self.assertEqual(type(result), dict)

    def test_call2_without_params(self):
        # with from
        test_call = CallBuilder().\
            from_(self.address).\
            to(self.to).\
            method("getStepCosts").\
            build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.to,
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                    "from": self.address
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=self.ret_json)
            result = self.icon_service.call(test_call)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
        self.assertEqual(type(result), dict)

    def test_call_without_from(self):
        # with from
        test_call = CallBuilder().\
            to(self.to).\
            method("getStepCosts").\
            params({}).\
            build()

        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                "jsonrpc": "2.0",
                "method": "icx_call",
                "id": 1234,
                "params": {
                    "to": self.to,
                    "dataType": "call",
                    "data": {
                        "method": "getStepCosts"
                    },
                }
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3", json=self.ret_json)
            result = self.icon_service.call(test_call)
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)
        self.assertEqual(type(result), dict)


if __name__ == "__main__":
    main()
