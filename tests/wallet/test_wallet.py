import copy
from typing import Union, Dict
from copy import deepcopy

import pytest

from iconsdk.wallet.wallet import KeyWallet, public_key_to_address, convert_public_key_format


class TestKeyWallet:

    @pytest.mark.parametrize(
        "compressed,hexadecimal,ret_type,size",
        (
            (True, True, str, 33),
            (True, False, bytes, 33),
            (False, True, str, 65),
            (False, False, bytes, 65),
        )
    )
    def test_get_public_key(self, compressed: bool, hexadecimal: bool, ret_type: type, size: int):
        wallet: KeyWallet = KeyWallet.create()
        public_key: Union[str, bytes] = wallet.get_public_key(compressed, hexadecimal)
        assert isinstance(public_key, ret_type)
        if hexadecimal:
            print(public_key)
            pub_key: bytes = bytes.fromhex(public_key)
            assert len(pub_key) == size
        else:
            assert len(public_key) == size

    def test_get_private_key(self):
        wallet: KeyWallet = KeyWallet.create()
        private_key: str = wallet.get_private_key()
        assert isinstance(private_key, str)
        assert not private_key.startswith("0x")

        private_key: bytes = wallet.get_private_key(hexadecimal=False)
        assert isinstance(private_key, bytes)
        assert wallet.private_key == private_key

    def test_private_key(self):
        wallet: KeyWallet = KeyWallet.create()
        wallet2: KeyWallet = KeyWallet.load(wallet.private_key)
        assert wallet == wallet2

        wallet3 = KeyWallet.create()
        assert wallet != wallet3

    def test_public_key(self):
        wallet: KeyWallet = KeyWallet.create()
        public_key: bytes = wallet.public_key
        assert isinstance(public_key, bytes)
        assert len(public_key) == 65

    def test_to_dict(self):
        password = "1234"
        wallet: KeyWallet = KeyWallet.create()
        jso: Dict[str, str] = wallet.to_dict(password)
        assert jso["address"] == wallet.get_address()
        assert jso["coinType"] == "icx"

        wallet2 = KeyWallet.from_dict(jso, password)
        assert wallet2 == wallet

    def test_copy(self):
        wallet = KeyWallet.create()
        wallet2 = copy.deepcopy(wallet)
        assert wallet == wallet2

        wallet3 = copy.copy(wallet)
        assert wallet == wallet3

    def test_hash(self):
        wallet = KeyWallet.create()
        wallet_dict = {wallet: wallet.public_key}
        assert wallet.public_key == wallet_dict[wallet]


def test_public_key_to_address():
    wallet: KeyWallet = KeyWallet.create()
    address: str = public_key_to_address(wallet.public_key)
    assert address == wallet.get_address()

    compressed_public_key: bytes = wallet.get_public_key(compressed=True, hexadecimal=False)
    address2: str = public_key_to_address(compressed_public_key)
    assert address2 == wallet.get_address()


@pytest.mark.parametrize(
    "iformat,oformat,size",
    (
        (True, True, 33),
        (True, False, 65),
        (False, True, 33),
        (False, False, 65),
    )
)
def test_convert_public_key_format(iformat: bool, oformat: bool, size: int):
    wallet: KeyWallet = KeyWallet.create()

    public_key: bytes = wallet.get_public_key(compressed=iformat, hexadecimal=False)
    ret: bytes = convert_public_key_format(public_key, compressed=oformat)
    if iformat == oformat:
        assert ret == public_key
    assert len(ret) == size
    assert public_key_to_address(public_key) == public_key_to_address(ret)
