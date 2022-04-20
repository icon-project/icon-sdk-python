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
from unittest import main
from unittest.mock import patch

import requests_mock

from tests.api_send.test_send_super import TestSendSuper


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestGetTotalSupply(TestSendSuper):

    def test_get_total_supply(self, _make_id):
        with requests_mock.Mocker() as m:
            supply = 1_000_000_000
            expected_request = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'icx_getTotalSupply',
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': hex(supply),
                'id': 1234
            }
            m.post(self.matcher, json=response_json)
            # case 0: when calling the method successfully
            result = self.icon_service.get_total_supply()
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request, actual_request)
            self.assertTrue(result, supply)

            # with height
            self.icon_service.get_total_supply(height=self.setting['height'])
            actual_request = json.loads(m._adapter.last_request.text)
            self.assertEqual(hex(self.setting['height']), actual_request['params']['height'])


if __name__ == "__main__":
    main()
