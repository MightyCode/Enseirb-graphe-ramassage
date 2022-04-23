import argparse


def giveArgsAndParser():
    parser = argparse.ArgumentParser(description="Graph project - Waste collector")
    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument("-N", "--size", nargs=2, type=int,
                       metavar=('width', 'height'),
                       help="Precise the size of the map.")

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument("-r", "--random", nargs=1, type=int,
                       metavar=('number'),
                       help="Generate a map with random positions of wastes. Should precise the number of wastes.")

    parser.add_argument("-p", "--path", type=str, nargs=1,
                        metavar="path",
                        help="Precise path of map used.")

    group = parser.add_mutually_exclusive_group(required=False)

    parser.add_argument("-s", "--seed", type=int, nargs=1,
                        metavar="sedd",
                        help="Set the seed for predictive randomness.")

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument("-c", "--sped", nargs=1, type=int,
                       metavar=('speed'),
                       help="Set the rotation speed of the robot in radian.")

    args = parser.parse_args()
    return [args, parser]

