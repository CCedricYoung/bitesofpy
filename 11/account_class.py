class Account:
    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    # add dunder methods below

    # length of the object: len(acc) returns the number of transactions
    def __len__(self) -> int:
        return len(self._transactions)

    # account comparison: acc1 >,<,>=.<=,== acc2 returns a boolean comparing account balances
    def __lt__(self, other: object) -> bool:
        return self.balance < other.balance

    def __le__(self, other: object) -> bool:
        return self.balance <= other.balance

    def __eq__(self, other: object) -> bool:
        return self.balance == other.balance

    def __ne__(self, other: object) -> bool:
        return self.balance != other.balance

    def __ge__(self, other: object) -> bool:
        return self.balance >= other.balance

    def __gt__(self, other: object) -> bool:
        return self.balance > other.balance

    # indexing: acc[n] shows the nth transaction onaccount (0 based)
    def __getitem__(self, index: int):
        return self._transactions[index]

    # iteration: list(acc) returns a sequence of account transactions
    def __reversed__(self):
        return self._transactions[::-1]

    # operator overloading: acc + int and acc - int can be used to add/subtract money (if given incompatible types for these operations, raise a TypeError - note that previously this was a ValueError, but former is more correct for this scenario)
    def __add__(self, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError

        self._transactions.append(amount)

    def __sub__(self, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError

        self._transactions.append(amount * -1)

    # string representation: str(acc) returns NAME account - balance: INT
    def __str__(self) -> str:
        return f"{self.name} account - balance: {self.balance}"
