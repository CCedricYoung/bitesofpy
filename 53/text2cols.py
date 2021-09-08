import itertools
import textwrap

COL_WIDTH = 20


def text_to_columns(text):
    """Split text (input arg) to columns, the amount of double
       newlines (\n\n) in text determines the amount of columns.
       Return a string with the column output like:
       line1\nline2\nline3\n ... etc ...
       See also the tests for more info."""
    
    paragraphs = text.split('\n\n')
    paragraphs = itertools.zip_longest(*[
        textwrap.wrap(x, width=COL_WIDTH)
        for x
        in paragraphs
    ], fillvalue=' ' * COL_WIDTH)
    paragraphs = ['     '.join([x.ljust(COL_WIDTH, ' ') for x in line]) for line in paragraphs]
    return('\n'.join(paragraphs))


text = """My house is small but cosy.

It has a white kitchen and an empty fridge.

I have a very comfortable couch, people love to sit on it."""

print(text_to_columns(text))
