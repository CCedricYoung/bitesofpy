from collections import namedtuple
from datetime import datetime

Transaction = namedtuple("Transaction", "giver points date")
# https://twitter.com/raymondh/status/953173419486359552
Transaction.__new__.__defaults__ = (datetime.now(),)


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self._transactions = []

    @property
    def points(self) -> int:
        return [x.points for x in self._transactions]

    @property
    def karma(self) -> int:
        return sum(self.points)

    @property
    def fans(self) -> int:
        return len({x.giver for x in self._transactions})

    def __add__(self, transactions: list):
        self._transactions.append(transactions)

    def __str__(self) -> str:
        fan = self.fans == 1 and 'fan' or 'fans'
        return f"{self.name} has a karma of {self.karma} and {self.fans} {fan}"
