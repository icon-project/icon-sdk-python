class IconService:

    def get_block(self, height_or_block_hash_or_latest: int):
        """
        If param is height, it is equivalent to icx_getBlockByHeight.
        Or block hash, it is equivalent to icx_getBlockByHash.
        Or string value same as `latest`, it is equivalent to icx_getLastBlock.

        :return: block
        """

    def get_total_supply(self):
        """It is equivalent to icx_getTotalSupply.

        :return:
        """

    def get_balance(self, address: str):
        """It is equivalent to icx_getBalance.

        :param address: str
        :return:d
        """

    def get_score_api(self, address: str):
        """It is equivalent to icx_getScoreApi.

        :param address:
        :return:
        """

    def get_transaction_result(self, tx_hash: str):
        """It is equivalent to icx_getTransactionResult.

        :param tx_hash:
        :return:
        """

    def get_transaction(self, tx_hash: str):
        """It is equivalent to icx_getTransactionByHash.

        :param tx_hash:
        :return:
        """
    def call(self, call: object):
        """It is equivalent to icx_call.

        :param call:
        :return:
        """

    def send_transaction(self, signed_transaction: object):
        """It is equivalent to icx_sendTransaction.

        :param signed_transaction:
        :return:
        """



