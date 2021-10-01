from collections import Counter


def calculate_gc_content(sequence):
    """
    Receives a DNA sequence (A, G, C, or T)
    Returns the percentage of GC content (rounded to the last two digits)
    """
    counts = {
        x:y
        for x, y
        in Counter(sequence.lower()).most_common()
    }
    total = sum([counts[x] for x in counts if x in 'agct'])
    result = round((counts['g'] + counts['c']) / total * 100, 2)
    return result
