import matplotlib.pyplot as plt
import numpy as np
import pmath
import loading

import permutations

if __name__ == "__main__":
    points : list = [[0,0],[1,2],[3,1],[6,5],[5,4],[5,8],[6,4],[5,2],[3,9]]  

    start: dict = {
        "position" : np.array([0.0, 0.0]),
        "angle" : np.array([0, 1]),
        "speedAngle" : 0.5 #rad/s
    }

    map = loading.load_map("rsc/map2.map")

    almost_complete_graph: list = loading.create_graph(map)

    position: list = []

    for i in range(1, len(almost_complete_graph)):
        position.append(pmath.getPosition(map, i))

    res = permutations.permuteAlgo(map["robot"],position,almost_complete_graph,5*60)
    lenghts : list = res[2]
    iterations : list = []
    for i in range(0,len(lenghts)):
        iterations.append(i)

    print(map)
    print(lenghts)
    print(iterations)

    plt.plot(iterations,lenghts)
    plt.xlabel("iterations")
    plt.ylabel("path length")
    plt.xticks(iterations)
    plt.show()