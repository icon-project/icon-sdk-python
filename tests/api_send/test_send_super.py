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

from os import path
from unittest import TestCase, main
from IconService.wallet.wallet import KeyWallet
from IconService.Icon_service import IconService
from IconService.providers.http_provider import HTTPProvider
from IconService.libs.in_memory_zip import gen_deploy_data_content
from tests.example_config import TEST_PRIVATE_KEY, TEST_HTTP_ENDPOINT_URI_V3


class TestSendSuper(TestCase):
    """
    A super class of other send test class, it is for unit tests of sending transaction.
    All of sup classes for testing sending transaction extends this super class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Sets needed data like an instance of a wallet and IconService
        and default values used to make 4 types of transactions. (transfer, call, deploy, message)
        """
        cls.wallet = KeyWallet.load(TEST_PRIVATE_KEY)
        cls.icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
        current_dir_path = path.abspath(path.dirname(__file__))
        score_path = path.join(current_dir_path, 'sample_token')
        install_content_bytes = gen_deploy_data_content(score_path)
        score_path = path.join(current_dir_path, 'sample_token2')
        update_content_bytes = gen_deploy_data_content(score_path)

        cls.setting = {
            "from": cls.wallet.get_address(),
            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
            "to_governance": "cx0000000000000000000000000000000000000001",
            "step_limit": 40000000,
            "nid": 3,
            "nonce": 2,
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
                "init_supply": 1000
            },
            # It is used to send message only.
            "data": "test"
        }


if __name__ == "__main__":
    main()


