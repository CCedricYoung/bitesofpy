from typing import List, Union
from itertools import cycle, chain


def join_lists(lst_of_lst: List[List[str]], sep: str) -> Union[List[str], None]:
    if not lst_of_lst:
        return None
    breakpoint()
    result =  list(chain.from_iterable(zip(lst_of_lst, cycle(sep))))[:-1]
    return result

join_lists([['a', 'b'], ['c'], ['d', 'e']], '+')