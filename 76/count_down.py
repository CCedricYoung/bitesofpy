from functools import singledispatch


@singledispatch
def count_down(counter):
    raise ValueError


@count_down.register
def _(counter: str):
    for x in reversed(range(1, len(counter) + 1)):
        print(counter[:x])


@count_down.register
def _(counter: int):
    count_down(str(counter))


@count_down.register
def _(counter: float):
    count_down(str(counter))


@count_down.register
def _(counter: list):
    count_down("".join(map(str, counter)))


@count_down.register
def _(counter: set):
    count_down(list(counter))


@count_down.register
def _(counter: tuple):
    count_down(list(counter))


@count_down.register
def _(counter: dict):
    count_down(list(counter.keys()))


@count_down.register
def _(counter: range):
    count_down(list(counter))
