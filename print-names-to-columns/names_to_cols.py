from typing import List  # not needed when we upgrade to 3.9


def print_names_to_columns(names: List[str], cols: int = 2) -> None:
    
    for ix, name in enumerate(names):
        if ix+1 == len(names):
            end = "\n"
        elif (ix + 1) % cols == 0:
            end = "\n"
        else:
            end = ""
        print(f"| {ix+1}{name:<10}", end=end)

print_names_to_columns(['John', 'Jane', 'Doe', 'Alice', 'Bob'], 2)



"""
| ix | name | mod 2|
| 0 | John | 0
| 1 | Jane | 1
| 2 | Doe  | 0
| 3 | Alice| 1
| 4 | Bob  | 0

"""