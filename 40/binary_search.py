def binary_search(sequence, target):
    start, end = 0, len(sequence) - 1

    while start <= end:
        mid = (start + end) // 2
        val = sequence[mid]
        if val == target:
            return mid

        if val < target:
            start = mid + 1
        else:
            end = mid - 1
