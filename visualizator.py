from os import name
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pmath

"""
Display a map and a graph using mathplotlib
map: Where with robot positions, wastes saved
graph: Connection betwenn points
name_plot: name displayed on the figure
"""
def display_map(map: dict, graph: list=[], name_plot="") -> None:
    min: list = [None, None]
    max: list = [None, None]

    position: list = []
    for i in range(len(graph)):
        position.append(pmath.getPosition(map, i))

        for j in [0, 1]:
            if min[j] == None or min[j] > position[i][j]:
                min[j] = position[i][j]
            
            if max[j] == None or max[j] < position[i][j]:
                max[j] = position[i][j]
    
    size: list = [max[0] - min[0], max[1] - min[0]]

    plt.xlim(min[0] - size[0] * 0.1, max[0] + size[0] * 0.1)
    plt.ylim(min[1] - size[1] * 0.1, max[1] + size[1] * 0.1)

    ax = plt.subplot()

    
    for obstacle in map["obstacles"]:
        rect = mpatches.Rectangle((obstacle["position"][0], obstacle["position"][1]), 
            obstacle["size"][0], obstacle["size"][1], alpha=0.6, facecolor="red")

        plt.gca().add_patch(rect)

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            index:int = graph[i][j]
            if index > i:
                plt.plot([position[i][0], position[index][0]], [position[i][1], position[index][1]], color="blue")

    i: int = 1
    for waste in map["wastes"]:
        ax.annotate(str(i), (waste["position"][0], waste["position"][1]))

        i += 1
    
    plt.plot(map["robot"]["position"][0], map["robot"]["position"][1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="red")

    plt.grid()
    plt.title(name_plot)
    plt.show()
    plt.close()
