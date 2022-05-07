from turtle import pos
import matplotlib.pyplot as plt
import pmath

def display_map(map: dict, graph: list=[], offset=5) -> None:
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

    plt.xlim(min[0] - offset, max[0] + offset)
    plt.ylim(min[1] - offset, max[0] + offset)

    ax = plt.subplot()

    for i in range(len(graph)):
        for j in graph[i]:
            print([position[i][0], position[j][0]], [position[j][0], position[j][1]])
            plt.plot([position[i][0], position[j][0]], [position[j][0], position[j][1]], color="blue")

    i: int = 1
    for waste in map["wastes"]:
        plt.plot(waste["position"][0], waste["position"][1], marker="o", markersize=3, markeredgecolor="black", markerfacecolor="green")
        ax.annotate(str(i), (waste["position"][0], waste["position"][1]))

        i += 1

    
    plt.plot(map["robot"]["position"][0], map["robot"]["position"][1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="red")

    plt.grid()
    plt.show()
