IMPOSSIBLE = 'Mission impossible. No one can contribute.'


def max_fund(village):
    """Find a contiguous subarray with the largest sum."""
    # Hint: while iterating, you could save the best_sum collected so far
    # return total, starting, ending
    best_sum, now_sum = 0, 0
    best_start, best_end = 0, 0

    for now_end, val in enumerate(village):
        if now_sum <= 0:
            now_sum = val
            now_start = now_end
        else:
            now_sum += val
        
        if now_sum > best_sum:
            best_sum, best_start, best_end = now_sum, now_start, now_end

    if best_sum == 0:
        print(IMPOSSIBLE)
        return 0, 0, 0

    return best_sum, best_start + 1, best_end + 1
