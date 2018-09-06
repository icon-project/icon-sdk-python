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

# data about returning block made from JSON RPC API V3 having multiple transactions.
block_v3_1 = {
    "version": "0.1a",
    "prev_block_hash": "cb0d9b334626c0c8436d61d719b80b5654a5f7fb244a31e6dcb8daf407428821",
    "merkle_tree_root_hash": "73b237ed527c1c9b0627510e2c7b7b495081a753991b5a872d5cdafcff318edf",
    "time_stamp": 1534488716612419,
    "confirmed_transaction_list": [
        {
            "version": "0x3",
            "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
            "value": "0xde0b6b3a7640000",
            "stepLimit": "0x12345",
            "timestamp": "0x5739bfed62373",
            "nid": "0x3",
            "nonce": "0x2",
            "signature": "NStjfPsF/PWKmYmLgPEegzxc0iPAn07bBwzXL1VEAcRD5OK7Ue2o3C9xP8cBm0hEKygjf2jVk2ElmktgkREsjAE=",
            "txHash": "0x4e00a7e4d60057a71ad405159380f766894d7baa3b9708c0de228456c46576bd"
        },
        {
            "version": "0x3",
            "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
            "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
            "value": "0xde0b6b3a7640000",
            "stepLimit": "0x12345",
            "timestamp": "0x5739bfed6f679",
            "nid": "0x3",
            "signature": "wxic8sFST7xRK6oIj6GOLZP3b7Y2Lu8zlkMwcdBpkEU8DECFogtkuHpEes3AnyTJBQ8NkJDzzwtp1q2pJ2EjaAA=",
            "txHash": "0xe4146fcec0f66c6ceb5a29f3616bbef9e168dae320825c346defc913f20ec0e0"
        }
    ],
    "block_hash": "3750f02d62fbe430c0b8cbdc1d8f5495f4f1dba01b9c7c7eef22d61f4cb6ae60",
    "height": 2,
    "peer_id": "hx86aba2210918a9b116973f3c4b27c41a54d5dafe",
    "signature": "47IPcUEVUniX+UZaZ1gAiPzwWbewifpkoZ3wysmYzRwj25HMkX4/wyikcmnYJZeao8hoT7/A+fvYpUwErRCewgA="
}

# data about returning block made from JSON RPC API V3 having a transaction.
block_v3_2 = {
        "version": "0.1a",
        "prev_block_hash": "60c5f2a3f303a0d3e2b19c507d378a987f8f0fb69995cd49a0d7abbcb94c6746",
        "merkle_tree_root_hash": "7deec308d57232108cafbebb0d1180900666784539d839d252e90ba8a005bf6b",
        "time_stamp": 1536050391146171,
        "confirmed_transaction_list": [
            {
                "version": "0x3",
                "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
                "stepLimit": "0xee6b2800",
                "timestamp": "0x5750799e3a085",
                "nid": "0x3",
                "to": "cx6d34efb31a521f680a77d736678de30ef9aff9ce",
                "dataType": "call",
                "data": {
                    "method": "transfer",
                    "params": {
                        "addr_to": "hxab2d8215eab14bc6bdd8bfb2c8151257032ecd8b",
                        "value": "0x1"
                    }
                },
                "signature": "mCe/44Hg+6dpbY45XiqKk1aOqHViUn3sDrvXG41HUWU3uYoxrPNLLAi7fhIOP84mj+OpICDD6oANN61tS0UKEwE=",
                "txHash": "0x6f1b39a956f87bf9ca18b54e5cfcc36e96b0d63db6bd4b19fad74b87c4bf62f4"
            },
            {
                "version": "0x3",
                "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
                "stepLimit": "0xee6b2800",
                "timestamp": "0x5750799e3e930",
                "nid": "0x3",
                "to": "cx0000000000000000000000000000000000000000",
                "dataType": "deploy",
                "data": {
                    "contentType": "application/zip",
                    "content": "0x504b03041400000008005095f44c504a3cd7270200005d0600005600000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f73616d706c655f746f6b656e2e70798d54516bdb30107ef7af107d899dae25632fc32c63c9b28741e80af106a31421dbe760aa4846524243e97fdfd99125258dd3e929d1f9befbbe4f775729b92175218506b5ab0b20f5a691ca9071144505675a9315db341c32f90422fe891fae0aa960ce34246914113c94ce67cbd9ddf71f2b3225a39c71260ad0231bcb7e65b3255dfdbebf5ffe6de3461ac6a9de360ddf8f0e00df6007c270b98e6b51c23394d34f491728a12299624257a0620dbcfa4058592a5a21e994ccf027686def8c0c6e768c6f2125b530494a1a5411393c4a6b511b4a2d5e99a7c4a95a30c3f25619b9f94aeea480b44b6b0f12460ec9ad4b2ff3c407110a23a13494fa87a9c53cb6b1d086b6aae548cdbe8169cbf314acf711811675613c526ff67914a7530a64aa9110b74a3bde07729d3308fc713299200c14f5867177f9f982fc00d5d66acf89f0a012196311321ef745a24b9edd6a3071783168ca43f77fa3d798822da31eb16a987864c3b6299981ce85cbcaec8749df95cf0694603c56c04a29f87e9aa92df8ce0c0b7a7434d1832b305b25ce6a5da3d6ffad646553590d4ec17bb59d732ef5319c09733c65f4dc98d1b7734683416b09e452f2d4bf715d1dca07fc3d7242bef4f92ec13db5c295a04c5c5dbdf884d791ee9dc0d49743eeeb55f2a6a79c569fdb36c8a5e88da5f20e9491c3406decba8739c6713bcc97f476f62e26a72fd7f6c04983f8de3bb3158736a07f9881b60cb182a172b0162d582e152e809c154f43437558b9d13f504b03041400000008005095f44c084d808322000000260000005200000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f5f5f696e69745f5f2e70794b2bcacf55d02b4ecc2dc8498d2fc9cf4ecd53c8cc2dc82f2a5108068b858084b800504b03041400000008005095f44c057d7c97420000005c0000005300000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f7061636b6167652e6a736f6eabe6520002a5b2d4a2e2ccfc3c252b0525033d033d43251d88786e62665e7c5a664e2a48a63831b7202735be243f3b350f454171727e115845305845085801572d00504b010214031400000008005095f44c504a3cd7270200005d060000560000000000000000000000a4810000000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f73616d706c655f746f6b656e2e7079504b010214031400000008005095f44c084d80832200000026000000520000000000000000000000a4819b02000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f5f5f696e69745f5f2e7079504b010214031400000008005095f44c057d7c97420000005c000000530000000000000000000000a4812d03000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f7061636b6167652e6a736f6e504b0506000000000300030085010000e00300000000"
                },
                "signature": "5d7GkuGTOOFT1E0yG+RUBxzNhFeQjT3gDARZZ98WlT0iFp7i5OnHnCnh2iSRUqcd0/SBNuuqqTPqSHlWecXxfgA=",
                "txHash": "0x6c41dce5b575dcf8142f890a6339c37898ebf78002a66d0f10e54d956048e484"
            },
            {
                "version": "0x3",
                "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
                "stepLimit": "0xee6b2800",
                "timestamp": "0x5750799e5c808",
                "nid": "0x3",
                "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
                "nonce": "0x3",
                "dataType": "message",
                "data": "0x74657374",
                "signature": "jgOTez0MxwgXsyZVi7vNjHyLmnpwMMHCmdnvHjeOnYAHfUcsfcHfh0uhyGgvTtlJSK+y4FhYI9hQJr4CtF+kGwE=",
                "txHash": "0x31029cae0878ab00cf5aa7ed988608a6136ee910ba17583b9fdc9f2b67de2eb1"
            },
            {
                "version": "0x3",
                "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
                "stepLimit": "0xee6b2800",
                "timestamp": "0x5750799e61691",
                "nid": "0x3",
                "to": "hx5bfdb090f43a808005ffc27c25b213145e80b7cd",
                "dataType": "message",
                "data": "0x74657374",
                "signature": "PYHIigN1eoS5y6LB/H3agfUF2bwK7ytzvsvU0zRbwdVDuawQGymZU0OClNDc4I1yxKWjpHOgysgzK0Wsx+2BYgA=",
                "txHash": "0x5f0aa6cd32e005d910525be53d0ac717cf99cd379bc5cfd969da6591a4f256de"
            }
        ],
        "block_hash": "f237e1839b3e0836ce305c67629441a7dd0dc47f05b10bb16d0d09157e26f73d",
        "height": 9,
        "peer_id": "hx86aba2210918a9b116973f3c4b27c41a54d5dafe",
        "signature": "rxez6oRdeWco/4aohUldQ+/sH60LAU6hHxHeIsCKqJEN9godDID04HtrOQeHonbutFWUSm9E23vp0Yaq11uRLAE="
    }

# data about returning block made from JSON RPC API V2 having multiple transactions.
block_v2_1 = {
    "version": "0.1a",
    "prev_block_hash": "12a8cff14a8d09880a8b7db260ce003b27138a888f02c4b175a626d87b4066b0",
    "merkle_tree_root_hash": "7a4de5dca7605444884073ed6d7b454e68954a2a3eae83a34956f1ed0147edf5",
    "time_stamp": 1536027997712760,
    "confirmed_transaction_list": [
        {
            "from": "hxebf3a409845cd09dcb5af31ed5be5e34e2af9433",
            "value": "0x6aaf7c8516d0c0000",
            "fee": "0x2386f26fc10000",
            "timestamp": "1536027997060029",
            "nonce": "1",
            "to": "hx2387149b9d9e58752b7bf8c5695221d9feb7274f",
            "signature": "ZLNdUWxvsiu74ggVkwODU2Z07m2YyUcIHeFE6wOVlvp9lFG7JdF0jopEZ7aOuj4UqXvg+67LEnO9NLiTa4vX7gE=",
            "tx_hash": "7a4de5dca7605444884073ed6d7b454e68954a2a3eae83a34956f1ed0147edf5",
            "method": "icx_sendTransaction"
        },
        {
            "from": "hx2387149b9d9e58752b7bf8c5695221d9feb7274f",
            "value": "0x1111d67bb1bb0000",
            "fee": "0x2386f26fc10000",
            "timestamp": "1536027998187226",
            "nonce": "1",
            "to": "hx6a12238188b19122de1655e7ec9f95975e8c36f8",
            "signature": "UR+lt5gwHymnCh3Kl2/3Eac1GLEC3nusDG97BNx3HAVMJmBXpmGmuUGL24VXpFmAvkjP3oB5iIHd+PXp4xjrCgA=",
            "tx_hash": "625db32336d85eaa38e578d2c71aa5951c495e5b79615b18149d10605a203672",
            "method": "icx_sendTransaction"
        }
    ],
    "block_hash": "e07969d741f7d20140696077f94e9f3efda55e86cdf73003168a155c463c48e7",
    "height": 1,
    "peer_id": "hx86aba2210918a9b116973f3c4b27c41a54d5dafe",
    "signature": "6co+1akQMN9ZScsukz3I+o8nTNVVYXS/xKcTTD2emVcG09wcY8zxi7t6pyBH8w+dzPw0rcDkPekNd72qHRJGWQE="
}

# data about returning block made from JSON RPC API V2 having a transaction.
block_v2_2 = {
    "version": "0.1a",
    "prev_block_hash": "e07969d741f7d20140696077f94e9f3efda55e86cdf73003168a155c463c48e7",
    "merkle_tree_root_hash": "625db32336d85eaa38e578d2c71aa5951c495e5b79615b18149d10605a203672",
    "time_stamp": 1536027998682443,
    "confirmed_transaction_list": [
        {
            "from": "hx2387149b9d9e58752b7bf8c5695221d9feb7274f",
            "value": "0x1111d67bb1bb0000",
            "fee": "0x2386f26fc10000",
            "timestamp": "1536027998187226",
            "nonce": "1",
            "to": "hx6a12238188b19122de1655e7ec9f95975e8c36f8",
            "signature": "UR+lt5gwHymnCh3Kl2/3Eac1GLEC3nusDG97BNx3HAVMJmBXpmGmuUGL24VXpFmAvkjP3oB5iIHd+PXp4xjrCgA=",
            "tx_hash": "625db32336d85eaa38e578d2c71aa5951c495e5b79615b18149d10605a203672",
            "method": "icx_sendTransaction"
        }
    ],
    "block_hash": "ad1c212f90591067fd667071fdf227ad657bfcedd0880ac63c95b2b65052ba09",
    "height": 2,
    "peer_id": "hx86aba2210918a9b116973f3c4b27c41a54d5dafe",
    "signature": "e9PQYWJRsepA9/CjOCgFsfGZLLRAXvgEyXj7usOyx5sPcwBI5bdB5YETmgWlPLHss1eU0vt3ZQk7qPQB6aevBAA="
}

block_v2_3 = {
     "version": "0.1a",
     "prev_block_hash": "357a42f19d4f86d39585b6cb17739f583a2254aed66a03d961a4de1475e04e7b",
     "merkle_tree_root_hash": "7d7b10198648a721d1ec4a23c4788a5e6ff1ca00d5c91f5f49fc9c13664176fc",
     "time_stamp": 1531184790261450,
     "confirmed_transaction_list": [{
       "tx_hash": "7d7b10198648a721d1ec4a23c4788a5e6ff1ca00d5c91f5f49fc9c13664176fc",
       "fee": "0x2386f26fc10000",
       "from": "hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
       "timestamp": 1531184789084451,
       "value": "0x1156abf16a40f0000",
       "to": "hxdc6a27bbc8cb124843527c000160ce075ca4d4c1",
       "signature": "Kbv4Azwy+h8jGezDpEhGg1crt6lsBv8fNa34YUV+FEtRA0lTN7Xw8Rn0WZjW4sqTgkvzyWcz6TV2FBtpSrJ1KwE=",
       "method": "icx_sendTransaction"
     }],
     "block_hash": "df760a42c6774c7bfd9d428dc3a2243afc7da04f96213cb761b0f463c1aca7e3",
     "height": 21265,
     "peer_id": "hxbda7906f9969af02cc81ca9b8088263bd4f26d7f",
     "signature": "66EIVpamui87ysXYYnZT6gp6MWN44STng9dO7tGip1cPSoMBs6yobwVl+T3yft0ttO8ksSiDv464Gu8SAn9UuQA="
}


# data about returning the genesis block.
# genesis block has not formatted transaction data.
block_genesis = {
    "version": "0.1a",
    "prev_block_hash": "",
    "merkle_tree_root_hash": "0ea9458bd24de3c1b754567f05afa10cfcb21b99f5bf9e45369b834cf9d280a4",
    "time_stamp": 0,
    "confirmed_transaction_list": [
        {
            "nid": "0x3",
            "accounts": [
                {
                    "name": "god",
                    "address": "hxebf3a409845cd09dcb5af31ed5be5e34e2af9433",
                    "balance": "0x2961ffa20dd47f5c4700000"
                },
                {
                    "name": "treasury",
                    "address": "hxd5775948cb745525d28ec8c1f0c84d73b38c78d4",
                    "balance": "0x0"
                },
                {
                    "name": "test1",
                    "address": "hx670e692ffd3d5587c36c3a9d8442f6d2a8fcc795",
                    "balance": "0xd3c21bcecceda1000000"
                },
                {
                    "name": "test2",
                    "address": "hxdc8d79453ba6516bc140b7f53b6b9a012da7ff10",
                    "balance": "0x0"
                },
                {
                    "name": "test3",
                    "address": "hxbedeeadea922dc7f196e22eaa763fb01aab0b64c",
                    "balance": "0x0"
                },
                {
                    "name": "test4",
                    "address": "hxa88d8addc6495e4c21b0dda5b0bf6c9108c98da6",
                    "balance": "0x0"
                },
                {
                    "name": "test5",
                    "address": "hx0260cc5b8777485b04e9dc938b1ee949910f41e1",
                    "balance": "0x0"
                },
                {
                    "name": "test6",
                    "address": "hx09e89b468a1cdfdd24441668204911502fa3add9",
                    "balance": "0x0"
                },
                {
                    "name": "test7",
                    "address": "hxeacd884f0e0b5b2e4a6b4ee87fa5184ab9f25cbe",
                    "balance": "0x0"
                },
                {
                    "name": "test8",
                    "address": "hxa943122f57c7c2af7416c1f2e1af46838ad0958f",
                    "balance": "0x0"
                },
                {
                    "name": "test9",
                    "address": "hxc0519e1c56030be070afc89fbf05783c89b15e2f",
                    "balance": "0x0"
                },
                {
                    "name": "test10",
                    "address": "hxcebc788d5b922b356a1dccadc384d36964e87165",
                    "balance": "0x0"
                },
                {
                    "name": "test11",
                    "address": "hx7f8f432ffdb5fc1d2df6dd452ca52eb719150f3c",
                    "balance": "0x0"
                },
                {
                    "name": "test12",
                    "address": "hxa6c4468032824092ecdb3de2bb66947d69e07b59",
                    "balance": "0x0"
                },
                {
                    "name": "test13",
                    "address": "hxc26d0b28b11732b38c0a2c0634283730258f272a",
                    "balance": "0x0"
                },
                {
                    "name": "test14",
                    "address": "hx695ddb2d1e78f012e3e271e95ffbe4cc8fcd133b",
                    "balance": "0x0"
                },
                {
                    "name": "test15",
                    "address": "hx80ab6b11b5d5c80448d011d10fb1a579c57e0a6c",
                    "balance": "0x0"
                },
                {
                    "name": "test16",
                    "address": "hxa9c7881a53f2245ed12238412940c6f54874c4e3",
                    "balance": "0x0"
                },
                {
                    "name": "test17",
                    "address": "hx4e53cffe116baaff5e1940a6a0c14ad54f7534f2",
                    "balance": "0x0"
                },
                {
                    "name": "test18",
                    "address": "hxbbef9e3942d3d5d83b5293b3cbc20940b459e3eb",
                    "balance": "0x0"
                }
            ],
            "message": "A rHizomE has no beGInning Or enD; it is alWays IN the miDDle, between tHings, interbeing, intermeZzO. ThE tree is fiLiatioN, but the rhizome is alliance, uniquelY alliance. The tree imposes the verb \"to be\" but the fabric of the rhizome is the conJUNction, \"AnD ... and ...and...\"THis conJunction carriEs enouGh force to shaKe and uproot the verb \"to be.\" Where are You goIng? Where are you coMing from? What are you heading for? These are totally useless questions.\n\n- 『Mille Plateaux』, Gilles Deleuze & Felix Guattari\n\n\"Hyperconnect the world\""
        }
    ],
    "block_hash": "12a8cff14a8d09880a8b7db260ce003b27138a888f02c4b175a626d87b4066b0",
    "height": 0,
    "peer_id": "",
    "signature": ""
}