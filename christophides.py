import commerce

def christophides(start: dict, graph: list, points: list, wastes_count: int) -> list:
    #print(points)
    #print("Start christophides")
    #print("Graph: ", graph)
    #print("Points: ", points)
    spanning_tree = compute_minimum_spanning_tree(graph, points)
    print("Spanning tree done\n", spanning_tree)
    odd_graph = compute_odd_degree_graph(spanning_tree)
    print("Odd degree graph done\n", odd_graph)
    minimal_coupling_graph = compute_minimal_coupling_graph(odd_graph)
    print("Minimal coupling graph done\n", minimal_coupling_graph)
    union = union_graph(spanning_tree, minimal_coupling_graph)
    print("Union graph done\n", union)
    cycle = eulerian_cycle(union)
    print("Eulerian cycle path done\n", cycle)

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
        for n in range(len(neighbors)):
            for v in range(len(in_zone)):
                if n in graph[v]:
                    d = commerce.dist(points[in_zone[v]], points[neighbors[n]])
                    if min_distance == -1 or min_distance > d:
                        min_distance = d
                        vSrc = in_zone[v]
                        vDst = neighbors[n]
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
    for _ in range(len(graph)):
        result = result + [[]]

    while True:
        b, w = find_augmenting_path(graph, result) 
        if not b:
            return result
        result = symmetric_difference(result, path_to_graph(graph, w))


def is_saturated(matching, index):
    return len(matching[index]) > 0

"""
    @return (bool, Graph)
"""
def find_augmenting_path(g: list, matching: list) -> tuple:
    not_saturated : list = []
    for i in range(len(g)):
        if not is_saturated(matching, i):
            not_saturated = not_saturated + [i]

    for i in range(len(not_saturated)):
        for j in range(len(not_saturated)):
            if i != j:
                b, p = find_augmenting_path_between_2_vertices(g, matching, not_saturated[i], not_saturated[j])
                if b:
                    return (b, p)

    return (False, [])

"""
    @return (bool, Graph)
"""
def find_augmenting_path_between_2_vertices(graph: list, coupling: list, v1: int, v2: int) -> tuple:
    result : list = [v1]
    currentVertex = v1
    i = 0
    needEdgeInCoupling = False
    while currentVertex != v2:
        if i >= len(graph):
            if currentVertex == v1:
                return (False, [])
            i = currentVertex + 1
            result = result[:-1]
            currentVertex = result[len(result)-1]
            needEdgeInCoupling = not needEdgeInCoupling
        elif i not in result and i != currentVertex and i in graph[currentVertex] and (needEdgeInCoupling == (i in coupling[currentVertex])):
            result = result + [i]
            needEdgeInCoupling = not needEdgeInCoupling
            currentVertex = i
            i = 0
        else:
            i = i + 1

    return (True, result)

"""
    @return Graph
"""
def path_to_graph(original_graph: list, path: list) -> list:
    result : list = []
    for _ in range(len(original_graph)):
        result = result + [[]]

    for i in range(len(path)-1):
        result[path[i]].append(path[i+1])
        result[path[i+1]].append(path[i])

    return result


"""
    @return Graph
"""
def symmetric_difference(g1: list, g2 : list) -> list:
    result : list = []
    for _ in range(len(g1)):
        result = result + [[]]

    for i in range(0, len(g1)):
        for j in range(0, len(g1[i])):                
            if g1[i][j] not in g2[i]:
                result[i].append(g1[i][j])

    for i in range(0, len(g2)):
        for j in range(0, len(g2[i])):                
            if g2[i][j] not in g1[i]:
                result[i].append(g2[i][j])

    return result

"""
def existsAlternatedGrowingPath(graph):
    for index in range(len(graph)):
        if not is_saturated(graph, index):
            return True
    return False
"""

"""
    @return Graph
"""
def union_graph(graph1: list, graph2: list) -> list:
    result : list = []

    for i in range(len(graph1)):
        result.append(graph1[i].copy())
        result[i].extend(graph2[i].copy())
        result[i] = list(result[i]) # This is maybe better
        #result[i] = list(set(result[i]))
        result[i].sort()

    return result

"""
    @param Graph

    @return Cycle such as : [ 1, 2, 3, 1, 4, 5, 1 ]
"""
def eulerian_cycle(graph: list) -> list:
    #print("Graph: ", graph)
    result : list = []
    explorated : list = []
    for _ in range(len(graph)):
        explorated = explorated + [[]]

    def dfs(start: int, result: list):
        #print("dfs start=",start," result=",result)
        for c in graph[start]:
            if c not in explorated[start]:
                explorated[start].insert(0, c)
                explorated[c].insert(0, start)
                dfs(c, result)
        result.insert(0, start)

    dfs(0, result)
    result = result + [0]
    #print("result=",result)

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
    points = [[0.5, 0.5], [0, 0], [1, 0], [0, 1], [1, 1]]
    graph = [[1, 2, 3, 4], [0, 2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]]

    print("Local tests")

    print("Minimum Spanning Tree: ", compute_minimum_spanning_tree(graph, points))
    
    print("Odd degree: ", compute_odd_degree_graph([[2], [2], [0, 1, 3, 4], [2], [2]]))

    print("Union vertices: ", union_graph([[1], [0], []], [[1, 2], [0], [0]]))

    print("Eulerian Cycle: ", eulerian_cycle([[1, 2, 3, 4], [0, 2], [0, 1], [0, 4], [0, 3]]))

    print("Multiple vertices: ", remove_multiple_vertices(eulerian_cycle([[1, 2, 3, 4], [0, 2], [0, 1], [0, 4], [0, 3]])))

    print("Symmetric Difference: ", symmetric_difference([[3, 1], [0, 2], [1], [0]], [[3, 2], [3], [0], [0, 1]]))

    print("Find Augmenting Path: ", find_augmenting_path(compute_odd_degree_graph([[2], [2], [0, 1, 3, 4], [2], [2]]), [[], [], [], [], []]))

    print("Minimal Coupling Graph: ", compute_minimal_coupling_graph(compute_odd_degree_graph([[2], [2], [0, 1, 3, 4], [2], [2]])))

    print("\nTest with complete graph with 5 vertices")

    spanning_tree: list = compute_minimum_spanning_tree(graph, points)
    print(spanning_tree)

    odd_graph: list = compute_odd_degree_graph(spanning_tree)
    print(spanning_tree)

    minimal_coupling_graph: list = compute_minimal_coupling_graph(odd_graph)
    print(minimal_coupling_graph)

    union: list = union_graph(spanning_tree, minimal_coupling_graph)
    print(union)

    cycle: list = eulerian_cycle(union)
    print(cycle)

    without_mutiple: list = remove_multiple_vertices(cycle)
    print(without_mutiple)



