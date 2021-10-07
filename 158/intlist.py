import statistics
from numbers import Number
from typing import Iterable, List, Union


class IntList(list):
    def _get_int(obj: object) -> int:
        if not isinstance(obj, Number):
            raise TypeError

        return int(obj)

    def __add__(self, other: Union[Number, Iterable[Number]]) -> List[int]:
        if isinstance(other, Iterable):
            int_list = [IntList._get_int(x) for x in other]
            return super().__add__(int_list)
        else:
            return super().__add__([IntList._get_int(other)])

    def __iadd__(self, other: Union[Number, Iterable[Number]]) -> List[int]:
        if isinstance(other, Iterable):
            int_list = [IntList._get_int(x) for x in other]
            return super().__iadd__(int_list)
        else:
            return super().__iadd__([IntList._get_int(other)])

    def append(self, other: int) -> None:
        self.__iadd__(other)

    @property
    def mean(self):
        return statistics.mean(self)

    @property
    def median(self):
        return statistics.median(self)
