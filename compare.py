import matplotlib.pyplot as plt
import numpy as np
import generate
import pmath
import loading

import permutations
import commerce
import christophides

if __name__ == "__main__":

    TIME_LIMIT : int = 60*1000

    #empty lists which will containt path length for different number of wastes
    _christophides : list = []
    _commerce : list = []
    _permutations : list = []

    #abcissa of the plot
    iterations : list = []

    #variables that will be results of the different algorithms calls
    path1 : float 
    path2 : float
    path3 : float

    map : dict = {}
    position : list = []
    almost_complete_graph : list = []

    for i in range(2,20):
        map = generate.createAndGenerateMap([50,50],i)

        almost_complete_graph = loading.create_graph(map)

        for i in range(1, len(almost_complete_graph)):
            position.append(pmath.getPosition(map, i))
        
        ###
        path1 : list = permutations.permuteAlgo(map["robot"],position,almost_complete_graph, TIME_LIMIT)[0]

        ###
        #path2 : list = commerce.optimisation(map["robot"], np.array(position), almost_complete_graph, len(map["wastes"]), TIME_LIMIT)

        ###
        copy : list = position.copy()
        copy.insert(0, map["robot"]["position"])
        path3: list = christophides.christophides(map["robot"], almost_complete_graph, copy, 0)

        _permutations.append(commerce.distance_path_and_start(map["robot"],np.array(position),path1))
        """
        for i in range(len(path2)):
            path2[i]-=1
        """   
        for i in range(len(path3)):
            path3[i]-=1
        
        #_commerce.append(commerce.distance_path_and_start(map["robot"],np.array(position),path2))
        _christophides.append(commerce.distance_path_and_start(map["robot"],np.array(position),path3))

        iterations.append(i)

        position = []

    #plt.plot(iterations,_commerce,'r', label='brute force')
    plt.plot(iterations,_christophides,'b', label='christophides')
    plt.plot(iterations,_permutations,'g', label='permutations')

    plt.xlabel("number of wastes")
    plt.ylabel("path cost")
    plt.ylim([0,max(max(_christophides),max(_permutations))*1.1])
    plt.xticks(iterations)
    plt.title("path cost depeneding on an increasing number of wastes")
    plt.legend()
    plt.show()
    