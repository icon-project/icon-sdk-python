import enum
from unittest import main

from tests.api_send.test_send_super import TestSendSuper


class AccountFilter(enum.Flag):
    COIN = 1
    STAKE = 2
    DELEGATION = 4


class TestGetAccount(TestSendSuper):

    def test_get_account_coin(self):
        result: dict = self.icon_service.get_account(
            address=self.setting["from"],
            account_filter=AccountFilter.COIN.value,
        )
        expected_result: dict = {
            "coin": {
                'balance': '0x0',
                'flag': '0x0',
                'flagStr': 'CoinPartFlag.NONE',
                'type': '0x0',
                'typeStr': 'GENERAL'
            }
        }
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(expected_result, result)

    def test_get_account_stake(self):
        result: dict = self.icon_service.get_account(
            address=self.setting["from"],
            account_filter=AccountFilter.STAKE.value,
        )
        expected_result: dict = {
            "stake": {
                'stake': '0x0',
                'unstake': '0x0',
                'unstakeBlockHeight': '0x0',
                'unstakesInfo': []
            }
        }
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(expected_result, result)

    def test_get_account_delegation(self):
        result: dict = self.icon_service.get_account(
            address=self.setting["from"],
            account_filter=AccountFilter.DELEGATION.value,
        )
        expected_result: dict = {
            "delegation": {
                'delegations': [],
                'totalDelegated': '0x0'
            }
        }
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(expected_result, result)

    def test_get_account_all(self):
        all_filter: AccountFilter = AccountFilter.COIN | AccountFilter.STAKE | AccountFilter.DELEGATION
        result: dict = self.icon_service.get_account(
            address=self.setting["from"],
            account_filter=all_filter.value,
        )
        expected_result: dict = {
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
        }
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(expected_result, result)


if __name__ == "__main__":
    main()
