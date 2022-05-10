import generate
import loading
import visualizator
import argumentParser as ag 
import commerce
import pmath

import random


def main():
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
    
    almost_complete_graph: list = loading.create_graph(map)
    print(almost_complete_graph)

    # Change from complete graph to our path graph
    visualizator.display_map(map, almost_complete_graph)

    algorithm: int = 1
    if args.algorithm:
        algorithm = args.algorithm[0]
        if algorithm < 0 or algorithm > 2:
            print("Algorithm index invalide, please choose between 1 and 2 (included)")
            return 

    result: list = []


    if algorithm == 1:
        position: list = []

        for i in range(len(almost_complete_graph)):
            position.append(pmath.getPosition(map, i))

        print(position)

        result = commerce.optimisation(position, almost_complete_graph)

    visualizator.display_map(map, result)

if __name__ == "__main__":
    main()