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

transaction_v2_1 = {
        "from": "hxebf3a409845cd09dcb5af31ed5be5e34e2af9433",
        "value": "0x6aaf7c8516d0c0000",
        "fee": "0x2386f26fc10000",
        "timestamp": "1536027997060029",
        "nonce": "1",
        "to": "hx2387149b9d9e58752b7bf8c5695221d9feb7274f",
        "signature": "ZLNdUWxvsiu74ggVkwODU2Z07m2YyUcIHeFE6wOVlvp9lFG7JdF0jopEZ7aOuj4UqXvg+67LEnO9NLiTa4vX7gE=",
        "method": "icx_sendTransaction",
        "tx_hash": "7a4de5dca7605444884073ed6d7b454e68954a2a3eae83a34956f1ed0147edf5",
        "txIndex": "0x0",
        "blockHeight": "0x1",
        "blockHash": "0xe07969d741f7d20140696077f94e9f3efda55e86cdf73003168a155c463c48e7"
    }

transaction_v2_2 = {
        "from": "hx2387149b9d9e58752b7bf8c5695221d9feb7274f",
        "value": "0x1111d67bb1bb0000",
        "fee": "0x2386f26fc10000",
        "nonce": "1",
        # when timestamp field not exists
        "to": "hx6a12238188b19122de1655e7ec9f95975e8c36f8",
        "signature": "UR+lt5gwHymnCh3Kl2/3Eac1GLEC3nusDG97BNx3HAVMJmBXpmGmuUGL24VXpFmAvkjP3oB5iIHd+PXp4xjrCgA=",
        "method": "icx_sendTransaction",
        "tx_hash": "625db32336d85eaa38e578d2c71aa5951c495e5b79615b18149d10605a203672",
        "txIndex": "0x0",
        "blockHeight": "0x2",
        "blockHash": "0xad1c212f90591067fd667071fdf227ad657bfcedd0880ac63c95b2b65052ba09"
    }


transaction_v3_1 = {
        "version": "0x3",
        "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
        "stepLimit": "0xee6b2800",
        "timestamp": "0x5750799c2773f",
        "nid": "0x3",
        "to": "cx0000000000000000000000000000000000000000",
        "nonce": "0x3",
        "dataType": "deploy",
        "data": {
            "contentType": "application/zip",
            "content": "0x504b03041400000008005095f44c504a3cd7270200005d0600005600000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f73616d706c655f746f6b656e2e70798d54516bdb30107ef7af107d899dae25632fc32c63c9b28741e80af106a31421dbe760aa4846524243e97fdfd99125258dd3e929d1f9befbbe4f775729b92175218506b5ab0b20f5a691ca9071144505675a9315db341c32f90422fe891fae0aa960ce34246914113c94ce67cbd9ddf71f2b3225a39c71260ad0231bcb7e65b3255dfdbebf5ffe6de3461ac6a9de360ddf8f0e00df6007c270b98e6b51c23394d34f491728a12299624257a0620dbcfa4058592a5a21e994ccf027686def8c0c6e768c6f2125b530494a1a5411393c4a6b511b4a2d5e99a7c4a95a30c3f25619b9f94aeea480b44b6b0f12460ec9ad4b2ff3c407110a23a13494fa87a9c53cb6b1d086b6aae548cdbe8169cbf314acf711811675613c526ff67914a7530a64aa9110b74a3bde07729d3308fc713299200c14f5867177f9f982fc00d5d66acf89f0a012196311321ef745a24b9edd6a3071783168ca43f77fa3d798822da31eb16a987864c3b6299981ce85cbcaec8749df95cf0694603c56c04a29f87e9aa92df8ce0c0b7a7434d1832b305b25ce6a5da3d6ffad646553590d4ec17bb59d732ef5319c09733c65f4dc98d1b7734683416b09e452f2d4bf715d1dca07fc3d7242bef4f92ec13db5c295a04c5c5dbdf884d791ee9dc0d49743eeeb55f2a6a79c569fdb36c8a5e88da5f20e9491c3406decba8739c6713bcc97f476f62e26a72fd7f6c04983f8de3bb3158736a07f9881b60cb182a172b0162d582e152e809c154f43437558b9d13f504b03041400000008005095f44c084d808322000000260000005200000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f5f5f696e69745f5f2e70794b2bcacf55d02b4ecc2dc8498d2fc9cf4ecd53c8cc2dc82f2a5108068b858084b800504b03041400000008005095f44c057d7c97420000005c0000005300000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f7061636b6167652e6a736f6eabe6520002a5b2d4a2e2ccfc3c252b0525033d033d43251d88786e62665e7c5a664e2a48a63831b7202735be243f3b350f454171727e115845305845085801572d00504b010214031400000008005095f44c504a3cd7270200005d060000560000000000000000000000a4810000000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f73616d706c655f746f6b656e2e7079504b010214031400000008005095f44c084d80832200000026000000520000000000000000000000a4819b02000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f5f5f696e69745f5f2e7079504b010214031400000008005095f44c057d7c97420000005c000000530000000000000000000000a4812d03000055736572732f626f79656f6e2f5079636861726d50726f6a656374732f49636f6e507974686f6e53444b2f74657374732f6170695f73656e642f73616d706c655f746f6b656e2f7061636b6167652e6a736f6e504b0506000000000300030085010000e00300000000",
            "params": {
                "init_supply": "0x2710"
            }
        },
        "signature": "Y0dXJwf3It4cnsrMZjEa/YXAFf1YzmuKL95JnRcVjtR+PE1VebQXoE8NifRxnLFzk5GMIoZQ51Fbq+o6ZTSb2AA=",
        "txHash": "0x36d46e6f8ce3fb037f72c227214a391ba680fb771bb8062b7391a9ef084fdebc",
        "txIndex": "0x0",
        "blockHeight": "0x7",
        "blockHash": "0x6979f9ad26fcf54a59998337fe6383c1feb32ef111d0cc9b3a78eec595e1bf4e"
    }

transaction_v3_2 = {
        "version": "0x3",
        "from": "hx4873b94352c8c1f3b2f09aaeccea31ce9e90bd31",
        "stepLimit": "0xee6b2800",
        "timestamp": "0x5750799c32a42",
        "nid": "0x3",
        "to": "cx0000000000000000000000000000000000000001",
        "nonce": "0x3",
        "dataType": "call",
        "data": {
            "method": "acceptScore",
            "params": {
                "txHash": "0x36d46e6f8ce3fb037f72c227214a391ba680fb771bb8062b7391a9ef084fdebc"
            }
        },
        "signature": "dyGD5Zrf86iHSQjr60pWUzqUm+olfgO1FkLfeYsgDFF1lRKcVnhG4MN3I9pzNgGiOxiTQ9AGUKVHjaSHqHQr7QE=",
        "txHash": "0xd34941501ef27bd2eba6c35b382e5ca2da5f5e44bec3bf460367a8ee04fd3fae",
        "txIndex": "0x1",
        "blockHeight": "0x7",
        "blockHash": "0x6979f9ad26fcf54a59998337fe6383c1feb32ef111d0cc9b3a78eec595e1bf4e"
    }

transaction_v3_3 = {
        "version": "0x3",
        "from": "hxd9932b37df48b8a6fa6c17770c0137816e11c0bd",
        "value": "0x1111d67bb1bb0000",
        "stepLimit": "0x3000000",
        "timestamp": "0x57502666bbccc",
        "nid": "0x3",
        "nonce": "0x1",
        "to": "hxf1d9719d29488684039712e881830b5b37a64f11",
        "signature": "OW8/F9aHXXeq4N3/Xs8ZCBHFuZTIPWUz5PQijm07PGY5UXwKOJZQqqzDrOj3bQ9SOJc9upXC13QaFUbmgII1fgA=",
        "txHash": "0xa24ffb1152aa9c58dab9b9b2b7102d5b238e0076222991ba289581a63b6ac0a5",
        "txIndex": "0x0",
        "blockHeight": "0x4",
        "blockHash": "0x255822446aca1cf42e0a68302560f6f7e6e33ff9beea25c3ee23255bb5504165"
    }