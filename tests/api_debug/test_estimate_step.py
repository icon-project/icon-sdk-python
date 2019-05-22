from time import sleep

from iconsdk.builder.transaction_builder import DeployTransactionBuilder, CallTransactionBuilder
from iconsdk.builder.transaction_builder import TransactionBuilder, MessageTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from tests.api_send.test_send_super import TestSendSuper


class TestEstimateStep(TestSendSuper):

    def test_estimate_step_with_send_icx_transaction(self):
        # When having an optional property, nonce
        icx_transaction = TransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .value(self.setting["value"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(3) \
            .nonce(self.setting["nonce"]) \
            .version(3) \
            .build()

        self.assertEqual(100000, self.icon_service.estimate_step(icx_transaction))

    def test_estimate_step_with_message_transaction(self):
        # Checks if making an instance of message transaction correctly
        message_transaction = MessageTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .data(self.setting["data"]).build()

        self.assertEqual(102400, self.icon_service.estimate_step(message_transaction))

    def test_estimate_step_with_deploy_transaction(self):
        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()

        self.assertEqual(1042767600, self.icon_service.estimate_step(deploy_transaction))

    def test_estimate_step_with_call_transaction(self):

        param = {"init_supply": 10000}
        deploy_transaction = DeployTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_install"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .content_type(self.setting["content_type"]) \
            .content(self.setting["content_install"]) \
            .params(param) \
            .version(3) \
            .build()
        signed_transaction_dict = SignedTransaction(deploy_transaction, self.wallet)
        result_install = self.icon_service.send_transaction(signed_transaction_dict)
        sleep(2)
        installed_score_address = self.icon_service.get_transaction_result(result_install)["scoreAddress"]

        # Sends a call transaction calling a method `acceptScore` to make the SCORE active
        params = {"txHash": result_install}
        call_transaction = CallTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(self.setting["to_governance"]) \
            .step_limit(self.setting["step_limit"]) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .method("acceptScore") \
            .params(params) \
            .build()
        signed_transaction_dict = SignedTransaction(call_transaction, self.wallet)
        self.icon_service.send_transaction(signed_transaction_dict)

        params = {"addr_to": self.setting["to"], "value": 1000000}
        call_transaction = CallTransactionBuilder() \
            .from_(self.setting["from"]) \
            .to(installed_score_address) \
            .nid(self.setting["nid"]) \
            .nonce(self.setting["nonce"]) \
            .method("transfer") \
            .params(params) \
            .build()
        self.assertEqual(155160, self.icon_service.estimate_step(call_transaction))
