import enum
import json
from unittest import main

import requests_mock

from tests.api_send.test_send_super import TestSendSuper
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST


class AccountFilter(enum.Flag):
    COIN = 1
    STAKE = 2
    DELEGATION = 4


class TestGetAccount(TestSendSuper):
    def test_get_account_coin(self):
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_getAccount',
                'params': {
                    'address': self.setting["from"],
                    'filter': hex(AccountFilter.COIN.value)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "coin": {
                        'balance': '0x0',
                        'flag': '0x0',
                        'flagStr': 'CoinPartFlag.NONE',
                        'type': '0x0',
                        'typeStr': 'GENERAL'
                    }
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=expected_result)
            self.icon_service.get_account(
                address=self.setting["from"],
                account_filter=AccountFilter.COIN.value,
            )
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_account_stake(self):
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_getAccount',
                'params': {
                    'address': self.setting["from"],
                    'filter': hex(AccountFilter.STAKE.value)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "stake": {
                        'stake': '0x0',
                        'unstake': '0x0',
                        'unstakeBlockHeight': '0x0',
                        'unstakesInfo': []
                    }
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=expected_result)
            self.icon_service.get_account(
                address=self.setting["from"],
                account_filter=AccountFilter.STAKE.value,
            )
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_account_delegation(self):
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_getAccount',
                'params': {
                    'address': self.setting["from"],
                    'filter': hex(AccountFilter.DELEGATION.value)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "stake": {
                        'stake': '0x0',
                        'unstake': '0x0',
                        'unstakeBlockHeight': '0x0',
                        'unstakesInfo': []
                    }
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=expected_result)
            self.icon_service.get_account(
                address=self.setting["from"],
                account_filter=AccountFilter.DELEGATION.value,
            )
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)

    def test_get_account_all(self):
        all_filter: AccountFilter = AccountFilter.COIN | AccountFilter.STAKE | AccountFilter.DELEGATION
        with requests_mock.Mocker() as m:
            expected_request_body: dict = {
                'id': 1234,
                'jsonrpc': '2.0',
                'method': 'debug_getAccount',
                'params': {
                    'address': self.setting["from"],
                    'filter': hex(all_filter.value)
                }
            }
            expected_result: dict = {
                "jsonrpc": "2.0",
                "result": {
                    "coin": {
                        'balance': '0x0',
                        'flag': '0x0',
                        'flagStr': 'CoinPartFlag.NONE',
                        'type': '0x0',
                        'typeStr': 'GENERAL'
                    },
                    "stake": {
                        'stake': '0x0',
                        'unstake': '0x0',
                        'unstakeBlockHeight': '0x0',
                        'unstakesInfo': []
                    },
                    "delegation": {
                        'delegations': [],
                        'totalDelegated': '0x0'
                    }
                },
                "id": 1234
            }
            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/debug/v3", json=expected_result)
            self.icon_service.get_account(
                address=self.setting["from"],
                account_filter=all_filter.value,
            )
            actual_request_body = json.loads(m._adapter.last_request.text)
            self.assertEqual(expected_request_body, actual_request_body)


if __name__ == "__main__":
    main()
