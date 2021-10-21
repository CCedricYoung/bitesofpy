from functools import singledispatch


@singledispatch
def count_down(counter):
    raise ValueError


@count_down.register(str)
def _(counter: str):
    for x in reversed(range(1, len(counter) + 1)):
        print(counter[:x])


@count_down.register(int)
@count_down.register(float)
def _(counter):
    count_down(str(counter))


@count_down.register(list)
def _(counter: list):
    count_down("".join(map(str, counter)))


@count_down.register(set)
@count_down.register(tuple)
@count_down.register(dict)
@count_down.register(range)
def _(counter):
    count_down(list(counter))
