import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from math import sqrt, acos
import time
 
"""
Make a power of a
"""
def Sqr(a: float) -> float:
    return a * a


"""
Compute the distance between two points
p1: Point 1
p2: Point 2
"""
def dist(p1: list, p2: list) -> float:
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

"""
Compute the angle using three points
"""
def angle(p1: list, p2: list, p3: list) -> float:
    b: float = (dist(p1, p2) ** 2 + dist(p1, p3) ** 2 - dist(p3, p2) ** 2) / (2*dist(p1, p2)*dist(p2, p3))
    
    if (b > 1):
        b = 1

    return acos(b)


"""
Compute the angle using three points
"""
def angle2(p1: list, p2: list, p3: list) -> float:
    b: float = ((p1[0] - p2[0]) * (p2[0] - p3[0]) + (p1[1] - p2[1]) * (p2[1] - p3[1])) \
        / (sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) * sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2))
    if (b > 1):
        b = 1
    if (b < -1):
        b = -1
    return acos(b)

"""
Compute the angle between the robot initial position and angle and another point
start: robot information
p3: Point 3
"""
def angle_start(start: dict, p3: list):
    angle: float = start["angle"]
    pos: list = start["position"]

    if pos[0] == p3[0] and pos[1] == p3[1]:
        return 0
    b= (angle[0] * (pos[0] - p3[0]) 
    + angle[1] * (pos[1] - p3[1])) /sqrt(angle[0] ** 2 
    + angle[1] ** 2) * sqrt((pos[0] - p3[0]) ** 2 
    + (pos[1] - p3[1]) ** 2)
    if (b>1):
        b=1
    if (b<-1):
        b=-1

    return acos(b)

"""
Compute the cost of traveling between two points given a speedAngle
"""
def distance_between_two_points(start: dict, points: list, path: list) -> float:
    d = 0
    for i in range(1, len(points)-1):
        d += dist(points[path[i-1], :], points[path[i], :])
        d += angle2(points[path[i-1], :], points[path[i], :], points[path[i+1], :]) * start["speedAngle"]

    return d

"""
Compute the cost of a path given a list of points and a start
"""
def distance_path_and_start(start: dict, points: list, path: list) -> float:
    d = distance_between_two_points(start, points, path)

    d += dist(start["position"],points[path[0], :]) + angle_start(start, points[path[0], :]) * start["speedAngle"]
    + dist(start["position"], points[path[-1], :]) 
    + dist(points[path[-2], :], points[path[-1], :])

    return d


"""
Test plot points
"""
def plot_points(points, chemin):
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    loop = list(chemin) + [chemin[0]]
    p = points[loop]

    ax[0].plot(points[:, 0], points[:, 1], 'o')
    ax[1].plot(p[:, 0], p[:, 1], 'o-')
    ax[1].set_title("dist=%1.2f" % distance_path_and_start(points, chemin))
    return ax

"""
Indicate if a path is possible given a graph
permutation: The path
graph: Reference graph
"""
def possible(permutation: tuple, graph: list):
    for i in range(len(permutation) - 1):
        if permutation[i + 1] not in graph[permutation[i]]:
            return False

    return True

"""
Complete a path if is not possible to go from a to b given liaisons (which indicates how go from a to b)
path: Path
liaison: list of path to go from each a to each b
"""
def completePath(path, liaisons):
    i: int = 0
    while i < len(path) - 1:
        n1 = path[i]
        n2 = path[i + 1]

        liaison: list = liaisons[n1 if n1 < n2 else n2][n2 if n2 > n1 else n1]
        if n1 > n2:
            for j in range(len(liaison)):
                path.insert(i + 1, liaison[j])
        else:
            for j in range(len(liaison) -1, -1, -1):
                path.insert(i + 1, liaison[j])

        i += len(liaison) + 1


"""
Experimental | Not implemented | 
Compute a path from each a to b in a given graph
"""
def compute_paths(start: dict, points: list, graph: list, wastes_count: int) -> list:
    def find_best_path(src: int, dst: int) -> list:
        result: list = []

        return result

    result: list = []

    for i in range(wastes_count):
        result.append({})
        for j in range(wastes_count):
            if i < j:
                result[i][j] = find_best_path(i, j)

    return result

def path_including_start(path: list) -> list:
    result: list = [0]
    for i in path:
        result.append(i + 1)
    result.append(0)

    return result


"""
Using the brut force technic compute the most efficient path to visit each wastes
start: robot information
points: position of vertices (wastes + corner of obstacles)
graph: original graph
numberWastes: Number of wastes
limit: limit of time in second

"""
def optimisation(start: dict, points: list, graph: list, numberWastes: int, limit: int) -> list:
    dist = None
    best = None

    #Precaculs
    graph_without_robot = graph[1:]
    paths: dict = compute_paths(start, points, graph_without_robot, numberWastes)

    start_time: int = int(round(time.time() * 1000))

    for p in permutations(range(len(points))):
        #completePath(p, paths)

        true_path = path_including_start(p)
        if not possible(true_path, graph):
            continue
        
        d = distance_path_and_start(start, points, p)
        if dist == None or d < dist:
            dist = d
            best = p

        if int(round(time.time() * 1000)) - start_time > limit:
            print(int(round(time.time() * 1000)) - start_time)
            break
    
    if best == None:
        return []

    return path_including_start(best)

if __name__ == "__main__":
    paths = [
        {
            1 : [],
            2 : [4, 5],
            3 : [5]
        },
        {
            0 : [],
            2 : [4, 5],
            3 : [5]
        },
        {
            0 : [18],
            1 : [4, 5],
            3 : [5]
        },
    ]

    path = [0, 2, 1]
    completePath(path, paths)
    print(path)

    graph = [[1], [0, 2], [1]]

    print("Path possible : ", possible([0, 1, 2], graph))
    print("Path impossible : ",possible([0, 2, 1], graph))
    