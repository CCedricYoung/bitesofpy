def countdown():
    """Write a generator that counts from 100 to 1"""
    for x in reversed(range(1, 101)):
        yield x