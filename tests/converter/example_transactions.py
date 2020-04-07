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

"""Sample transactions for testing the converter which is returned by 'icx_getTransactionByHash'"""

TRANSACTION_0 = {
    "from": "hx54f7853dc6481b670caf69c5a27c7c8fe5be8269",
    "to": "hx49a23bd156932485471f582897bf1bec5f875751",
    "value": "0x56bc75e2d63100000",
    "fee": "0x2386f26fc10000",
    "nonce": "0x1",
    "txHash": "0x375540830d475a73b704cf8dee9fa9eba2798f9d2af1fa55a85482e48daefd3b",
    "signature": "bjarKeF3izGy469dpSciP3TT9caBQVYgHdaNgjY+8wJTOVSFm4o/ODXycFOdXUJcIwqvcE9If8x6Zmgt//XmkQE=",
    "method": "icx_sendTransaction",
    "txIndex": "0x0",
    "blockHeight": "0x1",
    "blockHash": "0x3add53134014e940f6f6010173781c4d8bd677d9931a697f962483e04a685e5c"
}

TRANSACTION_1 = {
    "from": "hx49a23bd156932485471f582897bf1bec5f875751",
    "to": "hx48ed23e910acd48a2650d83d4a7aeea0795572af",
    "value": "0x2b5e3af16b1880000",
    "fee": "0x2386f26fc10000",
    "timestamp": "1517997570352000",
    "txHash": "0x1b6133792cee1ab2e54ae68faf9f49daf81c7e46d68b1ca281acc718602c77dd",
    "signature": "WDq5KJw776+ZY1RpnDe6b3fE9R5lgrG7JH9CwM0OcNBhmUSY4k4c6i+4F0GwRf+HblFd27zcezA/g6C4PoebzQE=",
    "method": "icx_sendTransaction",
    "txIndex": "0x0",
    "blockHeight": "0x2",
    "blockHash": "0x2cd6b2a6edd6dbce861bd9b79e91b5bc8351e7c87430e93251dfcb309a8ecff8"
}

TRANSACTION_2 = {
    "from": "hx1ada76577eac29b1e60efee22aac66af9f434036",
    "to": "cx502c47463314f01e84b1b203c315180501eb2481",
    "version": "0x3",
    "nid": "0x1",
    "stepLimit": "0x7a120",
    "timestamp": "0x58a4594d8a1f8",
    "nonce": "0xa6b2",
    "dataType": "call",
    "data": {
        "method": "mint",
        "params": {
            "_to": "hx853010e3a5b950d50ab8f98895fbd4b35c549189",
            "_amount": "0x4563918244f40000"
        }
    },
    "signature": "vjkZEDPZCaQTrrdkbiDeJPD/htA5Yr9U9jEJa/RsnA58fX4QH7aoxTtRIbRR4pr6YKJ6ThTlYrZwCkOA8H/NcQE=",
    "txHash": "0xa18d3d130d57326a0df66818d333cd96147950ae5bcd644c7145018a3eefb317",
    "txIndex": "0x1",
    "blockHeight": "0x100300",
    "blockHash": "0xa712b7e57dd807c50cd9d28a5a9c70689f2fa62e9d55d5fced6120ab21428eec"
}

TRANSACTION_3 = {
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

TRANSACTION_4 = {
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

TRANSACTION_5 = {
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
