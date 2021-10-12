from collections import namedtuple
from enum import Enum
from typing import OrderedDict, Sequence

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points


class BridgeHand:
    def __init__(self, cards: Sequence[Card]):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """

        for x in cards:
            if not isinstance(x, Card):
                raise ValueError("Not an instance of Card")

        if len(cards) != 13:
            raise ValueError("Number of elements is not 13")

        self.cards = [
            "".join([rank.name for rank in Rank if Card(suit, rank) in cards])
            for suit in Suit
        ]

    def __str__(self) -> str:
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order.
        Separate the suit symbol from its cards with a colon, and
        the suits with a single space.
        Note that a "10" should be represented with a capital 'T'
        """
        suits = list(Suit)
        return " ".join(
            [f"{suits[k].name}:{v}" for k, v in enumerate(self.cards) if v != ""]
        )

    @property
    def hcp(self) -> int:
        """Return the number of high card points contained in this hand"""
        results = [HCP.get(Rank[y], 0) for x in self.cards for y in x]
        return sum(results)

    @property
    def doubletons(self) -> int:
        """Return the number of doubletons contained in this hand"""
        result = [x for x in self.cards if len(x) == 2]
        return len(result)

    @property
    def singletons(self) -> int:
        """Return the number of singletons contained in this hand"""
        result = [x for x in self.cards if len(x) == 1]
        return len(result)

    @property
    def voids(self) -> int:
        """Return the number of voids (missing suits) contained in
        this hand
        """
        result = [x for x in self.cards if len(x) == 0]
        return len(result)

    @property
    def ssp(self) -> int:
        """Return the number of short suit points in this hand.
        Doubletons are worth one point, singletons two points,
        voids 3 points
        """
        return self.doubletons + 2 * self.singletons + 3 * self.voids

    @property
    def total_points(self) -> int:
        """Return the total points (hcp and ssp) contained in this hand"""
        return self.hcp + self.ssp

    @property
    def ltc(self) -> int:
        """Return the losing trick count for this hand - see bite description
        for the procedure
        """
        result = 0
        for x in self.cards:
            ranks = x[:3]
            size = len(ranks)

            if size > 2 and ranks[2] not in "Q":
                result += 1
            if size > 1 and ranks[1] not in "KQ"[:size]:
                result += 1
            if size > 0 and ranks[0] not in "AKQ"[:size]:
                result += 1

        return result
