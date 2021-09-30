from collections import deque

def num_ops(n):
    """
    Input: an integer number, the target number
    Output: the minimum number of operations required to reach to n from 1.

    Two operations rules:
    1.  multiply by 2
    2.  int. divide by 3

    The base number is 1. Meaning the operation will always start with 1
    These rules can be run in any order, and can be run independently.

    [Hint] the data structure is the key to solve it efficiently.
    """
    prev = {0, 1}
    ops_num = 0
    queue = deque([(0, 1)])
    while queue:
        ops_num, val = queue.popleft()
        if val == n:
            return ops_num 

        div_val = val // 3
        if div_val not in prev:
            queue.append((ops_num + 1, div_val))
            prev.add(div_val)

        mul_val = val * 2
        if mul_val not in prev:
            queue.append((ops_num + 1, mul_val))
            prev.add(mul_val)

    return ops_num
