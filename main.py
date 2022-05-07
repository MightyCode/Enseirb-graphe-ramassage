import generate
import loading
import visualizator
import argumentParser as ag 

import random


def main():
    args, parser = ag.giveArgsAndParser()

    if not args.path and not args.random:
        print("No map path precised, or number of waste for a random map, -h for help.")
        return

    if args.seed:
        random.seed(args.seed)

    map: dict
    if args.path:
        map = loading.load_map(args.path[0], args.size if args.size else None)

    elif args.random:
        if not args.size:
            print("Map size should be precised if random map generated")
            return 

        map = generate.createAndGenerateMap(args.size, args.random[0])

    print(loading.create_graph(map))

    visualizator.display_map(map)

    print(map)

if __name__ == "__main__":
    main()