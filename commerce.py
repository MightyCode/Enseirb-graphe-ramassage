#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 15:40:24 2022

@author: facen
"""
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

def distance_chemin(points, chemin):
    d = 0
    for i in range(1, len(points)-1):
        #print(angle2(points[chemin[i-1], :], points[chemin[i], :], points[chemin[i+1], :])*180/pi)
        d += dist(points[chemin[i-1], :], points[chemin[i], :]) + angle2(points[chemin[i-1], :], points[chemin[i], :], 
                points[chemin[i+1], :])*100
    d += dist(points[chemin[0], :], points[chemin[-1], :]) + dist(points[chemin[-2], :], points[chemin[-1], :])

    return d


def plot_points(points, chemin):
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))

    loop = list(chemin) + [chemin[0]]
    p = points[loop]

    ax[0].plot(points[:, 0], points[:, 1], 'o')
    ax[1].plot(p[:, 0], p[:, 1], 'o-')
    ax[1].set_title("dist=%1.2f" % distance_chemin(points, chemin))
    return ax

def possible(permutation, graphe):
    for i in range(len(permutation) - 1):
        if permutation[i + 1] not in graphe[permutation[i]]:
            return False

    return True

def optimisation(points, graph) -> list:
    dist = None
    best = None

    for p in permutations(range(len(graph))):
        if not possible(p, graph):
            continue
        
        d = distance_chemin(points, p)
        if dist == None or d < dist:
            #print(d)
            dist = d
            best = p
    
    if best == None:
        return []


    result: list = []
    for i in range(len(graph) + 1):
        result.append([])

    # Start connected to first vertex and last    
    result[0].append(best[0] + 1)
    result[0].append(best[-1] + 1)
    result[best[0] + 1].append(0)
    result[best[-1] + 1].append(0)

    for i in range(len(best) - 1):
        result[best[i] + 1].append(best[i + 1] + 1)
        result[best[i + 1] + 1].append(best[i] + 1)
    
    return result

if __name__ == "__main__":
    points = np.array([[0,0],[0,12],[10,4],[10,8],[20,8],[20,4],[30,12],[30,0]])
    #points = numpy.random.random((6, 2))
    print(list(range(points.shape[0])))
    #res = optimisation(points, list(range(points.shape[0])))

    graph: list = []
    for i in range(len(points)):
        graph.append([])
        for j in range(len(points)):
            if i != j:
                graph[-1].append(j)

    res = optimisation(points, graph)
    plot_points(points, res)

