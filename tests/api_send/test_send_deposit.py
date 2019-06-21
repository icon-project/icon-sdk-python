from iconsdk.builder.transaction_builder import DepositTransactionBuilder, DepositTransaction
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.utils.validation import is_T_HASH
from tests.api_send.test_send_super import TestSendSuper


class TestSendDeposit(TestSendSuper):

    def test_add_deposit(self):
        # transaction instance for add action
        deposit_transaction_of_add_0: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .action("add") \
            .build()

        # Checks if sending transaction correctly
        signed_transaction_dict = SignedTransaction(deposit_transaction_of_add_0, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))

    def test_withdraw_deposit(self):
        # transaction instance for withdraw action
        deposit_transaction_of_withdraw_0: DepositTransaction = DepositTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .id(self.setting["id"]) \
            .action("withdraw") \
            .build()

        # Checks if sending transaction correctly
        signed_transaction_dict = SignedTransaction(deposit_transaction_of_withdraw_0, self.wallet)
        result = self.icon_service.send_transaction(signed_transaction_dict)
        self.assertTrue(is_T_HASH(result))
