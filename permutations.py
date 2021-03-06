import commerce

import numpy as np
import random
import time

# computes a random path using a set of points. Concretly, it shuffles the points list
def calculateFirstPath(points : list) -> list:
    path : list = []

    for i in range(0, len(points)):
        path.append(i)

    random.shuffle(path)
    return path

# swaps two edges
# the edge (path[i],path[i+1]) is swapped with the edge (path[j],path[j+1])
# PRECOND : i,j should be in ]0,len(points)-2[

def permuteTwoEdges(path: list, i1 : int, i2 : int):
    if (i1 > 0 and i1 < len(path) - 2 and i2 > 0 and i1 < len(path) - 2):
        pathList = path.copy()
        i1,i2 = min(i1,i2),max(i1,i2)

        edge1 : list = [pathList[i1],pathList[i1+1]]
        edge2 : list = [pathList[i2],pathList[i2+1]]

        copy : list = pathList[:i1+1]
        copy.append(pathList[i2])

        sub = pathList[i1+2:i2]
        sub.reverse()

        for i in sub:
            copy.append(i)

        copy.append(pathList[i1+1])
        copy.append(pathList[i2+1])

        for i in pathList[i2+2:]:
            copy.append(i)

        return copy
    else:
        print("indexes are not between 0 and len(points)-2")

# the 2-opt algorithm
# @param start : dict | the starting point of the robot
# @param points : list | wastes list
# @param graph : list | the graph describing the relations between every vertices
# @param LIMIT : int | a time limit. The algorithm will stop if this limit is reached

# @return best_path : list | the path founded by the algorithm
# @return best_len : float | the cost of the founded path
# @return length : list | a list describing the cost of the path at every permutations that reduces the cost
def permuteAlgo(start : dict, points : list, graph: list, LIMIT : int) -> tuple :
    np_points = np.array(points)

    best_path: list = calculateFirstPath(points)
    best_len: int = commerce.distance_path_and_start(start, np_points, best_path)

    iteration: int = 0

    lengths : list = []

    start_time: int = int(round(time.time() * 1000))
    while iteration < 1000 and int(round(time.time() * 1000)) - start_time < LIMIT:
        print("                                          ", end="\r")
        print("Iteration", iteration, best_len, end="\r")
        np_path: list = calculateFirstPath(points)
        pathLen: int = commerce.distance_path_and_start(start, np_points, np_path)

        if pathLen < best_len and """commerce.possible(newPath, graph)""":
            best_path = np_path.copy()
            best_len = pathLen

        local_cmp: int = -1
        tmp_cmp: int = 0
        
        while tmp_cmp != local_cmp:
            local_cmp = tmp_cmp
            

            for i in range(1, len(np_path) - 2):
                for j in range(1, len(np_path) - 2):
                    if(j >= i + 2 or j <= i - 2):
                        newPath = permuteTwoEdges(np_path, i, j)
                        newPathLength: int = commerce.distance_path_and_start(start, np_points, newPath)

                        if newPathLength < best_len and """commerce.possible(newPath, graph)""":
                            tmp_cmp = tmp_cmp + 1
                            best_len = newPathLength
                            best_path = newPath.copy()
                            lengths.append(best_len)
                        
        iteration += 1
    return best_path, best_len, lengths
if __name__ == "__main__":
    points : list = [[0,0],[1,2],[3,1],[6,5],[5,4],[5,8],[6,4],[5,2],[3,9]]  

    start: dict = {
        "position" : np.array([0.0, 0.0]),
        "angle" : np.array([0, 1]),
        "speedAngle" : 0.5 #rad/s
    }

    print("points :",points)

    path = calculateFirstPath(points)
    print("first path :",path)
    res = permuteAlgo(start,points)
    print("final result :")
    print("path :",res[0])
    print("length of the path :",res[1])
    print("number of permutations computed :",res[2])
