from os import stat
import commerce

def christophides(start: dict, graph: list, points: list, wastes_count: int) -> list:
    
    spanning_tree = compute_minimum_spanning_tree(graph, points)

    odd_graph = compute_odd_degree_graph(spanning_tree)

    minimal_coupling_graph = compute_minimal_coupling_graph(odd_graph)

    union = union_graph(spanning_tree, minimal_coupling_graph)

    cycle = eulerian_cycle(union)

    return remove_multiple_vertices(cycle)

"""
    @return Graph
"""
def compute_minimum_spanning_tree(graph: list, points: list) -> list:
    result : list = []
    for _ in range(len(graph)):
        result = result + [[]]
    neighbors : list = graph[0]
    in_zone : list = [0]
    while len(neighbors) > 0:
        #print("in_zone: " + str(in_zone)[1:-1] )
        #print("result: " + str(result)[1:-1] )
        #print("neighbors: " + str(neighbors)[1:-1] )
        min_distance = -1
        vSrc = 0
        vDst = 0
        for n in neighbors:
            for v in range(len(result)):
                if n in graph[v]:
                    d = commerce.dist(points[v], points[n])
                    if min_distance == -1 or min_distance > d:
                        min_distance = d
                        vSrc = v
                        vDst = n
        result[vSrc] = result[vSrc] + [vDst]
        result[vDst] = result[vDst] + [vSrc]
        in_zone = in_zone + [vDst]
        neighbors = neighbors + graph[n]
        tmp_neighbors = []
        for i in range(len(neighbors)):
            if neighbors[i] not in tmp_neighbors and neighbors[i] not in in_zone:
                tmp_neighbors = tmp_neighbors + [neighbors[i]]
        neighbors = tmp_neighbors
    return result

"""
    @return Graph
"""
def compute_odd_degree_graph(graph: list) -> list:
    result : list = []

    odd: list = []

    for i in range(len(graph)):
        if len(graph[i]) % 2 == 1:
            odd.append(i)

    for i in range(len(graph)):
        result.append([])

        if i in odd:
            for j in odd:
                if i != j:
                    result[i].append(j)

    return result

"""
    @return Graph
"""
def compute_minimal_coupling_graph(graph: list) -> list:
    result : list = []
    return result

"""
    @return Graph
"""
def union_graph(graph1: list, graph2: list) -> list:
    result : list = []

    for i in range(len(graph1)):
        result.append(graph1[i].copy())
        result[i].extend(graph2[i].copy())
        result[i] = list(set(result[i]))
        result[i].sort()

    return result

"""
    @parap Graph

    @return Cycle such as : [ 1, 2, 3, 1, 4, 5, 1 ]
"""
def eulerian_cycle(graph: list) -> list:
    result : list = []
    explorated : list = []
    for _ in range(len(graph)):
        explorated = explorated + [[]]

    def dfs(start: int, result: list):
        for c in graph[start]:
            if c not in explorated[start]:
                explorated[start] = explorated[start] + [c]
                dfs(c, result)
        result.insert(0, start)

    dfs(0, result)

    return result

"""
    @param Cycle such as : [ 1, 2, 3, 1, 4, 5, 1 ]

    @return Cycle such as : [ 1, 2, 3, 4, 5, 1 ]
"""
def remove_multiple_vertices(cycle: list) -> list:
    result : list = []
    for i in range(0, len(cycle)-1):
        if cycle[i] not in result:
            result = result + [cycle[i]]
    return result + [cycle[0]]


if __name__ == "__main__":
    #points = [ [0,0], [0,1], [3,0], [0,-2] ]

    #print("Minimum Spanning Tree: ", compute_minimum_spanning_tree([[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], points))
    
    #print("Odd degree: ", compute_odd_degree_graph([[2], [2], [0, 1, 3, 4], [2], [2]]))

    #print("Union vertices: ", union_graph([[1], [0], []], [[1, 2], [0], [0]]))

    print("Eulerian Cycle: ", eulerian_cycle([[1, 2, 3, 4], [0, 2], [0, 1], [0, 4], [0, 3]]))

    print("Multiple vertices: ", remove_multiple_vertices(eulerian_cycle([[1, 2, 3, 4], [0, 2], [0, 1], [0, 4], [0, 3]])))
