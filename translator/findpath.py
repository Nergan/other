from heapq import heappop, heappush


def findpath(beg, end, graph):
    if beg == end:
        return [[beg, end]]
    
    nodes = list(graph.keys())
    n = len(nodes)
    index_map = {node: idx for idx, node in enumerate(nodes)}
    dist = [float('inf')] * n
    prev = [None] * n
    dist[index_map[beg]] = 0
    heap = [(0, beg)]
    
    while heap:
        d, u = heappop(heap)
        u_idx = index_map[u]
        if d != dist[u_idx]:
            continue
        if u == end:
            path = []
            current = end
            while prev[index_map[current]] is not None:
                path.append([prev[index_map[current]], current])
                current = prev[index_map[current]]
            path.reverse()
            return path
        for v, weight in graph[u].items():
            if weight == 0:
                continue
            v_idx = index_map[v]
            new_d = d + weight
            if new_d < dist[v_idx]:
                dist[v_idx] = new_d
                prev[v_idx] = u
                heappush(heap, (new_d, v))
                
    return None