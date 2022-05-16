import matplotlib.pyplot as plt
import numpy as np
import pmath
import loading

import permutations

if __name__ == "__main__":
    #loading map 2
    map = loading.load_map("rsc/map2.map")

    almost_complete_graph: list = loading.create_graph(map)

    position: list = []

    for i in range(1, len(almost_complete_graph)):
        position.append(pmath.getPosition(map, i))

    res = permutations.permuteAlgo(map["robot"],position,almost_complete_graph, 60 * 1000)
    lenghts : list = res[2]
    iterations : list = []
    for i in range(0,len(lenghts)):
        iterations.append(i)

    plt.plot(iterations,lenghts)
    plt.xlabel("number of permutations done")
    plt.ylabel("path length")
    plt.xticks(iterations)
    plt.ylim([0,max(lenghts)*1.1])
    plt.title("Path length computed for every iterations, for map 2")
    plt.show()