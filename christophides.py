def christophides(start: dict, graph: list, points: list, wastes_count: int) -> list:
    spanning_tree = compute_minimum_spanning_tree(graph)

    odd_graph = compute_odd_degree_graph(spanning_tree)

    minimal_coupling_graph = compute_minimal_coupling_graph(odd_graph)

    union = union_graph(spanning_tree, minimal_coupling_graph)

    cycle = eulerian_cycle(union)

    return remove_multiple_vertices(cycle)

"""
    @return Graph
"""
def compute_minimum_spanning_tree(graph: list) -> list:
    result : list = []
    
    return result

"""
    @return Graph
"""
def compute_odd_degree_graph(graph: list) -> list:
    result : list = []
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
    return result

"""
    @parap Graph

    @return Cycle such as : [ 1, 2, 3, 1, 4, 5, 1 ]
"""
def eulerian_cycle(graph) -> list:
    result : list = []
    return result

"""
    @param Cycle such as : [ 1, 2, 3, 1, 4, 5, 1 ]

    @return Cycle such as : [ 1, 2, 3, 4, 5, 1 ]
"""
def remove_multiple_vertices(cycle: list) -> list:
    result : list = []
    return result
