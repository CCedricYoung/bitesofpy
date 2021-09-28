from typing import List


def pascal(N: int) -> List[int]:
    """
    Return the Nth row of Pascal triangle
    """
    rows = [0 for _ in range(N + 1)]
    rows[1] = 1

    for i in range(1, N + 1):
        for j in range(i, 0, -1):
            rows[j] += rows[j - 1]

    return rows[1:]
