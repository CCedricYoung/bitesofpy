import pprint
from typing import Any, Iterable


def pretty_string(obj: Any, level: int = 0) -> str:
    return pprint.pformat(obj, width=60, depth=2, sort_dicts=True)
