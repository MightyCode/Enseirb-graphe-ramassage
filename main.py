import generate
import loading
import visualizator
import argumentParser as ag 
import commerce
import permutations
import christophides
import pmath

import random
import numpy as np
import time

def main():
    start: int = int(round(time.time() * 1000))
    total: int = 0
    current_time: int = 0  

    limit_time = 5 * 60 * 1000

    args, parser = ag.giveArgsAndParser()

    if not args.path and not args.random:
        print("No map path precised, or number of waste for a random map, -h for help.")
        return

    if args.seed:
        print(args.seed[0])
        random.seed(args.seed[0])

    map: dict
    if args.path:
        map = loading.load_map(args.path[0], args.size if args.size else None)

    elif args.random:
        if not args.size:
            print("Map size should be precised if random map generated")
            return 

        map = generate.createAndGenerateMap(args.size, args.random[0])
    
    if args.speed:
        map["robot"]["speedAngle"] = args.speed[0]

    almost_complete_graph: list = loading.create_graph(map)
    empty_graph: list = []
    for i in range(len(almost_complete_graph)):
        empty_graph.append([])

    
    current_time: int = int(round(time.time() * 1000))
    total += current_time - start

    # Change from complete graph to our path graph
    visualizator.display_map(map, empty_graph, "Affichage des déchets sans liaisons")
    visualizator.display_map(map, almost_complete_graph, "Affichage du graphe des chemins possibles")
    start = int(round(time.time() * 1000))

    algorithm: int = 3
    if args.algorithm:
        algorithm = args.algorithm[0]
        if algorithm < 0 or algorithm > 3:
            print("Algorithm index invalide, please choose between 1 and 2 (included)")
            return 

    result: list = []
    path: list = []
    position: list = []

    for i in range(1, len(almost_complete_graph)):
        position.append(pmath.getPosition(map, i))

    print("Begin algo")

    name = "Affichage du chemin trouvée"

    if algorithm == 1:
        result: list = commerce.optimisation(map["robot"], np.array(position), almost_complete_graph, len(map["wastes"]), limit_time - total)
        path: list = result[0]

        name += " : coût " + str(result[1])
    if algorithm == 2:
        result: list = permutations.permuteAlgo(map["robot"], position, almost_complete_graph, limit_time - total)
        path: list = result[0]
        
        for i in range(len(path)):
            path[i] += 1

        path.insert(0, 0)
        path.append(0)

        name += " : coût " + str(result[1])

    if algorithm == 3:
        position.insert(0, map["robot"]["position"])
        path = christophides.christophides(map["robot"], almost_complete_graph, position, 0)

    print("Begin end")
    print(path)

    result = pmath.path_to_graph(len(almost_complete_graph), path)

    current_time: int = int(round(time.time() * 1000))
    total += current_time - start
    visualizator.display_map(map, result, name)
    start = int(round(time.time() * 1000))

    current_time: int = int(round(time.time() * 1000))
    total += current_time - start

    print("Time taken : ", total / 1000)

if __name__ == "__main__":
    main()