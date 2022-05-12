#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from re import A
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from math import perm, sqrt,acos,pi
 
def Sqr(a):
    return a*a


def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def angle(p1, p2, p3):
    b=(dist(p1, p2) ** 2 + dist(p1, p3) ** 2 - dist(p3, p2) ** 2) / (2*dist(p1, p2)*dist(p2, p3))
    if (b>1):
        b=1
    return acos(b)


def angle2(p1, p2, p3):
    b = ((p1[0] - p2[0]) * (p2[0] - p3[0]) + (p1[1] - p2[1]) * (p2[1] - p3[1])) / (sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) * sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2))
    if (b>1):
        b=1
    if (b<-1):
        b=-1
    return acos(b)

def angle_depart(start, p3):
    angle = start["angle"]
    pos = start["position"]
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

def distance_between_two_points(start, points, path):
    d = 0
    for i in range(1, len(points)-1):
        d += dist(points[path[i-1], :], points[path[i], :])
        d += angle2(points[path[i-1], :], points[path[i], :], points[path[i+1], :]) * start["speedAngle"]

def distance_path_and_start(start, points, path):
    d = distance_between_two_points(start, points, path)

    d += dist(start["position"],points[path[0], :]) + angle_depart(start , points[path[0], :]) * start["speedAngle"]
    + dist(start["position"], points[path[-1], :]) 
    + dist(points[path[-2], :], points[path[-1], :])

    return d


def plot_points(points, chemin):
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    loop = list(chemin) + [chemin[0]]
    p = points[loop]

    ax[0].plot(points[:, 0], points[:, 1], 'o')
    ax[1].plot(p[:, 0], p[:, 1], 'o-')
    ax[1].set_title("dist=%1.2f" % distance_path_and_start(points, chemin))
    return ax

def possible(permutation, graphe):
    for i in range(len(permutation) - 1):
        if permutation[i + 1] not in graphe[permutation[i]]:
            return False

    return True

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
        print(i)


def optimisation(start, points, graph, numberWastes) -> list:
    dist = None
    best = None

    #Precaculs
    paths: dict = [[]  * numberWastes]

    for p in permutations(range(numberWastes)):
        p = completePath(p, paths)
        
        d = distance_path_and_start(start, points, p)
        if dist == None or d < dist:
            #print(d)
            dist = d
            best = p
    
    if best == None:
        return []

    path: list = [0]
    for i in best:
        path.append(i + 1)
    path.append(0)

    return path

if __name__ == "__main__":
    points = np.array([[0,0],[0,12],[10,4],[10,8],[20,8],[20,4],[30,12],[30,0]])
    #points = numpy.random.random((6, 2))
    start: dict = {
    "position" : np.array([0.0, 0.0]),
    "angle" : np.array([0, 1]),
    "speedAngle" : 0.5 #rad/s
    }
    #print(list(range(points.shape[0])))
    #res = optimisation(points, list(range(points.shape[0])))

    graph: list = []
    for i in range(len(points)):
        graph.append([])
        for j in range(len(points)):
            if i != j:
                graph[-1].append(j)

    res = optimisation(points, graph)
    #plot_points(points, res)

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
    