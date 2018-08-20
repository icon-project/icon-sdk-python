from iconservice import *


class SampleToken(IconScoreBase):

    __BALANCES = 'balances'
    __TOTAL_SUPPLY = 'total_supply'

    @eventlog(indexed=3)
    def Transfer(self, addr_from: Address, addr_to: Address, value: int): pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self.__total_supply = VarDB(self.__TOTAL_SUPPLY, db, value_type=int)
        self.__balances = DictDB(self.__BALANCES, db, value_type=int)

    def on_install(self, init_supply: int = 1000, decimal: int = 18) -> None:
        super().on_install()

        total_supply = init_supply * 10 ** decimal

        self.__total_supply.set(total_supply)
        self.__balances[self.msg.sender] = total_supply

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def total_supply(self) -> int:
        return self.__total_supply.get()

    @external(readonly=True)
    def balance_of(self, addr_from: Address) -> int:
        return self.__balances[addr_from]

    def __transfer(self, _addr_from: Address, _addr_to: Address, _value: int) -> bool:

        if self.balance_of(_addr_from) < _value:
            self.revert(f"{_addr_from}'s balance < {_value}")

        self.__balances[_addr_from] = self.__balances[_addr_from] - _value
        self.__balances[_addr_to] = self.__balances[_addr_to] + _value

        self.Transfer(_addr_from, _addr_to, _value)
        return True

    @external
    def transfer(self, addr_to: Address, value: int) -> bool:
        return self.__transfer(self.msg.sender, addr_to, value)

    def fallback(self) -> None:
        pass


