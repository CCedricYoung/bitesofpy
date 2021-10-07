from dataclasses import dataclass, field
from typing import List, Tuple

bites: List[int] = [283, 282, 281, 263, 255, 230, 216, 204, 197, 196, 195]
names: List[str] = [
    "snow",
    "natalia",
    "alex",
    "maquina",
    "maria",
    "tim",
    "kenneth",
    "fred",
    "james",
    "sara",
    "sam",
]


@dataclass
class Ninja:
    """
    The Ninja class will have the following features:

    string: name
    integer: bites
    support <, >, and ==, based on bites
    print out in the following format: [469] bob
    """

    def __init__(self, name: str, bites: int) -> None:
        self.name = name
        self.bites = bites

    def __str__(self) -> str:
        return f"[{self.bites}] {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: object) -> bool:
        return self.bites < other.bites

    def __gt__(self, other: object) -> bool:
        return self.bites > other.bites

    def __eq__(self, other: object) -> bool:
        return self.bites == other.bites


@dataclass
class Rankings:
    """
    The Rankings class will have the following features:

    method: add() that adds a Ninja object to the rankings
    method: dump() that removes/dumps the lowest ranking Ninja from Rankings
    method: highest() returns the highest ranking Ninja, but it takes an optional
            count parameter indicating how many of the highest ranking Ninjas to return
    method: lowest(), the same as highest but returns the lowest ranking Ninjas, also
            supports an optional count parameter
    returns how many Ninjas are in Rankings when len() is called on it
    method: pair_up(), pairs up study partners, takes an optional count
            parameter indicating how many Ninjas to pair up
    returns List containing tuples of the paired up Ninja objects
    """

    ninjas: list = field(default_factory=list)

    def add(self, other: Ninja) -> None:
        self.ninjas.append(other)
        self.ninjas.sort(reverse=True)

    def dump(self) -> None:
        if self.ninjas:
            return self.ninjas.pop()

    def highest(self, count: int = 1) -> List[Ninja]:
        return self.ninjas and self.ninjas[:count] or None

    def lowest(self, count: int = 1) -> List[Ninja]:
        return self.ninjas and self.ninjas[-1 : -1 * count - 1 : -1] or None

    def __len__(self) -> int:
        return len(self.ninjas)

    def pair_up(self, count: int = 3) -> List[tuple]:
        return list(zip(self.highest(count), self.lowest(count)))
