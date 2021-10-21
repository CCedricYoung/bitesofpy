PYBITES = "pybites"


def convert_pybites_chars(text):
    """Swap case all characters in the word pybites for the given text.
    Return the resulting string."""
    result = list(text)
    for x, v in enumerate(text):
        result[x] = (
            v.lower() in PYBITES and v.swapcase() or v
        )

    return "".join(result)
