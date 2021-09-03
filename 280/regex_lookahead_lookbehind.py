import re

def count_n_repetitions(text, n=1):
    """
    Counts how often characters are followed by themselves for
    n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    """
    regex = r'(.)(?=\1{' + str(n) + '})'
    return len(re.findall(regex,text, re.DOTALL))

inputs = [
    # ("333", 1), ("333", 2), ("3444553333", 2)
    ("", 1), # 0
    ("1112345", 2), # 1
    ("????{{{?}}}", 1), # 7
    ("\n\n\nAs are newlines\n\n\n", 2), # 2
]
for x in inputs:
    print(x, count_n_repetitions(*x))

def count_n_reps_or_n_chars_following(text, n=1, char=""):
    """
    Counts how often characters are repeated for n times, or
    followed by char n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    char: Character which also counts if repeated n times
    """

    if char == '':
        return count_n_repetitions(text, n)

    regex = f'(.)(?=\\1{{{n}}}|[{re.escape(char)}]{{{n}}})'
    return len(re.findall(regex, text, re.DOTALL))

inputs = [
    # ("3335567", 2,"5"), # 2
    # ("aa", 1,"a"), # 1
    # ("4455???", 2,"?"), # 2
    ("zz Don't count double!", 1, "z"),  # 1
    ("9z", 1, "z"),  # 1
    ("9zz", 1, "z"),  # 2
    ("9Zz", 1, "Z"),  # 1
    ("????{{{?}}}", 1, "?"),  # 8
    ("????[[[?]]]", 1, "["),  # 8
    ("????[[[?]]]", 1, "]"),  # 8
    ("Hello^there", 1, "^"),  # 2
    ("\n\n\nzz newlines\n\n", 2, "z"),  # 2
    ("Kai is mean...aarg", 2, "a"),  # 2
    ("But bob isn't...\t\t", 2, "\t"),  # 2
]
# for x in inputs:
#     print(x, count_n_reps_or_n_chars_following(*x))

def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
    letters = ''.join(map(re.escape, surrounding_chars))
    regex = f'(?<=[{letters}]).(?=[{letters}])'
    # print(text, surrounding_chars, regex)
    return len(re.findall(regex, text, re.DOTALL))

inputs = [
    # ("ZZZZZ", ["Z"]), # 3
    # ("ABCCBAAAZz", ["Z", "A"]), # 2
    # ("ZZZZZ", ["Z", "A"]), # 3
    # ("ABCCBAAAZz", ["Z", "A"]), # 2
    # ("\nK\nA\tI\t", ["\n", "\t"]), # 3
    # ("SPECIAL^C^HARS?", ["R", "?", "^"]), # 2
    # ("^S^tar$t$", ["^", "$"]), # 2
    # ("?:A:lmost|t|here", [":", "|"]), # 2

]
# for x in inputs:
#     print(check_surrounding_chars(*x))

