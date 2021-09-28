def count_islands(grid):
    """
    Input: 2D matrix, each item is [x, y] -> row, col.
    Output: number of islands, or 0 if found none.
    Notes: island is denoted by 1, ocean by 0 islands is counted by continuously
        connected vertically or horizontally  by '1's.
    It's also preferred to check/mark the visited islands:
    - eg. using the helper function - mark_islands().
    """
    islands = 0         # var. for the counts
    queue = {(i,j) for i in range(len(grid)) for j in range(len(grid[0]))}

    while len(queue) > 0:
        i, j = queue.pop()
        if grid[i][j] != 1:
            continue

        mark_islands(i, j, grid, queue)
        islands += 1
    
    return islands

def mark_islands(i, j, grid, queue):
    """
    Input: the row, column, grid and queue
    Output: None.
    Side-effects: Grid marked with visited islands.
        Visited paths removed from queue.
    """

    grid[i][j] = '#'
    DIRECTIONS = [(1, 0), (-1, 0), (0,1), (0,-1)]
    paths = [(i + d[0], j + d[1]) for d in DIRECTIONS]
    for path in paths:
        if path not in queue or grid[path[0]][path[1]] == 0:
            continue

        queue.remove(path)
        grid[path[0]][path[1]] = '#'
        mark_islands(*path, grid, queue)
