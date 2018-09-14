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
from threading import Timer
from time import sleep
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.utils.convert_type import convert_hex_str_to_int
from quickstart.examples.test.constant import TEST_HTTP_ENDPOINT_URI_V3


icon_service = IconService(HTTPProvider(TEST_HTTP_ENDPOINT_URI_V3))
wallet = KeyWallet.load("./test/test_keystore", "abcd1234*")


class RepeatedTimer(object):
    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.func(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def scan_forward_block(_time: int=100000, _interval: int=1):
    """Scans forward block"""
    pre_last_height = icon_service.get_block("latest")["height"]
    print(f"Starts to scan forward block at block height({pre_last_height})")

    def find_new_block():
        """Finds generating new block since the pre last block and prints it"""
        last_block = icon_service.get_block("latest")
        last_height = last_block["height"]
        nonlocal pre_last_height
        if last_height > pre_last_height:
            for height in range(pre_last_height + 1, last_height + 1):
                print("="*100)
                print("block height: ", height)
                block = icon_service.get_block(height)
                get_financial_transaction(block)
        pre_last_height = last_height

    # Starts repeated timer
    try:
        rt = RepeatedTimer(_interval, find_new_block)  # It auto-starts, no need of rt.start()
        sleep(_time)
    finally:
        rt.stop()
        

def get_financial_transaction(block):
    """
    Gets specific meaningful transactions and prints it.

    [What is the specific meaningful transaction]
    - First, finds ICX transactions on a block.
    - Second, finds token transfer on a block.  """
    tx_list = block["confirmed_transaction_list"]

    if len(tx_list) > 0:
        for tx in tx_list:
            print("\ntxHash:", tx["txHash"])
            tx_result = icon_service.get_transaction_result(tx["txHash"])

            # Finds ICX transaction
            if "value" in tx and tx["value"] > 0:
                print("[ICX]")
                print("status: ", tx_result["status"])
                print("from  : ", tx["from"])
                print("to    : ", tx["to"])
                print("amount: ", tx["value"])

            # Finds token transfer
            if "dataType" in tx and tx["dataType"] == "call" and "method" in tx["data"] and tx["data"]["method"] == "transfer":
                score_address = tx["to"]
                print(f"[{get_token_name(score_address)} Token({get_token_symbol(score_address)})]")
                print("status: ", tx_result["status"])
                print("from  : ", tx["from"])
                print("to    : ", tx["data"]["params"]["_to"])
                print("amount: ", convert_hex_str_to_int(tx["data"]["params"]["_value"]))


def get_token_name(token_address: str):
    """
    Gets the token name

    If not have the external method `name` to get the score name,
    it will raise JSONRPCException.
    """
    call = CallBuilder()\
        .from_(wallet.get_address())\
        .to(token_address)\
        .method("name")\
        .build()
    return icon_service.call(call)


def get_token_symbol(token_address: str):
    """
    Gets the token symbol

    If not have the external method `symbol` to get the score symbol,
    it will raise JSONRPCException.
    """
    call = CallBuilder()\
        .from_(wallet.get_address())\
        .to(token_address)\
        .method("symbol")\
        .build()
    return icon_service.call(call)


scan_forward_block(1000, 1)