from typing import List
from collections import deque


def make_changes(n: int, coins: List[int]) -> int:
    """
    Input: n - the changes amount
          coins - the coin denominations
    Output: how many ways to make this changes
    """

    val_to_coin = {y: x for x, y in enumerate(coins)}
    queue = deque([(0, [0] * len(coins))])
    ways = deque()
    seen = set()
    while queue:
        val, change = queue.pop()
        if val == n:
            if change not in ways:
                ways.append(change)
            continue

        for x in coins:
            new_change = change.copy()
            new_change[val_to_coin[x]] += 1
            key = " ".join(map(str, new_change))

            if val + x > n or key in seen:
                continue

            queue.append((val + x, new_change))
            seen.add(key)

    return len(ways)