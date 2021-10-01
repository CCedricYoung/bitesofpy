from itertools import permutations
import itertools
from typing import List, Union, Iterable


def find_all_solutions(
    operator_path: List[str], expected_result: int
) -> Union[List[List[int]], Iterable[List[int]]]:
    """
    list(find_all_solutions(["*", "*", "+"], 181))
    [
        [4, 5, 9, 1], # 4 * 5 * 9 + 1 = 181
        [4, 9, 5, 1], # 4 * 9 * 5 + 1 = 181
        [5, 4, 9, 1], # 5 * 4 * 9 + 1 = 181
        [5, 9, 4, 1], # 5 * 9 * 4 + 1 = 181
        [9, 4, 5, 1], # 9 * 4 * 5 + 1 = 181
        [9, 5, 4, 1], # 9 * 5 * 4 + 1 = 181
    ]
    - [1-9] used only once per solution
    - Using operators other than  +, - or * should raise a ValueError.
    - Using non int as a result should raise ValueError.
    - Make sure to implement the order of operations correctly (multiplication before addition or subtraction)
    """

    if len([x for x in operator_path if x not in "*+-"]) > 0:
        raise ValueError

    if not isinstance(expected_result, int):
        raise ValueError

    for x in permutations("123456789", len(operator_path) + 1):
        expression = " ".join(
            itertools.chain.from_iterable(
                itertools.zip_longest(x, operator_path, fillvalue="")
            )
        )
        val = eval(expression)
        if val == expected_result:
            yield list(map(int, x))