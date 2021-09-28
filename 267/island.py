# Hint:
# You can define a helper funtion: get_others(map, row, col) to assist you.
# Then in the main island_size function just call it when traversing the map.


def get_others(map_, r, c, valid_locs):
    """Go through the map and check the size of the island
    (= summing up all the 1s that are part of the island)

    Input - the map, row, column position
    Output - return the total number)
    """
    nums = 0

    map_[r][c] = "#"
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    others = [(r + d[0], c + d[1]) for d in DIRS]
    for loc in others:
        if loc not in valid_locs or map_[loc[0]][loc[1]] == 0:
            nums += 1
            continue

        if map_[loc[0]][loc[1]] == "#":
            continue

        map_[loc[0]][loc[1]] = "#"
        nums += get_others(map_, *loc, valid_locs)

    return nums


def island_size(map_):
    """Hint: use the get_others helper

    Input: the map
    Output: the perimeter of the island
    """

    valid_locs = {(i, j) for i in range(len(map_)) for j in range(len(map_[0]))}
    for loc in valid_locs:
        if map_[loc[0]][loc[1]] == 1:
            return get_others(map_, *loc, valid_locs)

    return 0
