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
from tests.api_send.test_send_super import TestSendSuper


class TestFullResponseBase(TestSendSuper):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.block: dict = {
            "version": "0.5",
            "height": 6226175,
            "signature": "pZc4zwOLky4JzSf9bxrY+UmMc3M/BM8v0/YrkmI5VyFiwoOXX5tXe+sp66Iz/dtFtYVBKgo0gZfIL3PSUROrMgE=",
            "prev_block_hash": "146eee45320f4eb7e0eeae2a7c3f7c5b70c2780383927964eb0386ae235ba6c0",
            "merkle_tree_root_hash": "9c9993ebf71cb4d4184b564ba3425a1535e65c9ae4029686d5976b2410f55c17",
            "time_stamp": 1598939091830275,
            "confirmed_transaction_list": [
                {
                    "version": "0x3",
                    "timestamp": "0x5ae3a04960603",
                    "dataType": "base",
                    "data": {
                        "prep": {
                            "irep": "0xa968163f0a57b400000",
                            "rrep": "0x449",
                            "totalDelegation": "0x18d92fa3589e6608f707c9",
                            "value": "0x24a9c0534f5126dc"
                        },
                        "result": {
                            "coveredByFee": "0x0",
                            "coveredByOverIssuedICX": "0x0",
                            "issue": "0x24a9c0534f5126dc"
                        }
                    },
                    "txHash": "0x9c9993ebf71cb4d4184b564ba3425a1535e65c9ae4029686d5976b2410f55c17"
                }
            ],
            "block_hash": "3c9d91c2ea42d6b20edd39093a5c4c6f332fa9cb381c29533399365e4c07916d",
            "peer_id": "hxd3be921dfe193cd49ed7494a53743044e3376cd3",
            "next_leader": "hxd3be921dfe193cd49ed7494a53743044e3376cd3"
        }

        cls.transaction = {
              "version": "0x3",
              "from": cls.setting["from"],
              "to": cls.setting["to"],
              "stepLimit": hex(cls.setting["step_limit"]),
              "value": "0x470de4df820000",
              "nid": hex(cls.setting["nid"]),
              "timestamp": "1517999520286000",
              "signature": "sILBL1MPwOou8ItM4s0Vqx21l62QyucgTLsEQ51BGi5v/IJ1hOCT/P/rz1V1pDSGAnTQ7rGw9rSOVM5TAGbJOAE=",
              "method": "icx_sendTransaction",
              "txHash": "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388",
              "txIndex": "0x0",
              "blockHeight": "0xa",
              "blockHash": "0x9a39a75d7075687f746d61191baf1a1ff3b5bc0acc4a8df0bb872e53e13cdc17"
        }

        cls.receipt = {
            "txHash": "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388",
            "blockHeight": "0x13f",
            "blockHash": "0x069e8a2431ae2c7e55924af477be87518476aa1eb1b2e7d1ee8d61d7874ea907",
            "txIndex": "0x1",
            "to": "cx0000000000000000000000000000000000000000",
            "stepUsed": "0x263b8",
            "stepPrice": "0x2540be400",
            "cumulativeStepUsed": "0x263b8",
            "eventLogs": [
                {
                    "scoreAddress": "cx0000000000000000000000000000000000000000",
                    "indexed": [
                        "PRepSet(Address)"
                    ],
                    "data": [
                        "hx86aba2210918a9b116973f3c4b27c41a54d5dafe"
                    ]
                }
            ],
            "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000080000000000000000000000000000000000000000000000000000000000020000000000000008000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "status": "0x1"
        }

        cls.block_hash = "0x3c9d91c2ea42d6b20edd39093a5c4c6f332fa9cb381c29533399365e4c07916d"
        cls.block_height = 6226175
        cls.transaction_hash = "0x33db06f38424207daa69c9df153649fd3913c21e162f16f4839c9c3318e44388"
