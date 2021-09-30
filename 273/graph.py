import heapq


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """

    queue = [(0, [start])]
    while queue:
        val, path = heapq.heappop(queue)

        if path[-1] == end:
            return (val, path)
        
        for dest, cost in graph[path[-1]].items():
            heapq.heappush(queue,(val + cost, path + [dest]))
