import re

def get_sentences(text):
    """Return a list of sentences as extracted from the text passed in.
       A sentence starts with [A-Z] and ends with [.?!]"""
    return re.split(r'(?<=[.?!]) (?=[A-Z])', text.replace('\n', ' ').strip())
