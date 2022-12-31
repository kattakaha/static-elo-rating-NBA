import sys

import staticelo.controller.calc


def main(argc, argv):

    if argc != 3:
        print("invalid input.")
        return

    season = argv[1]
    K = int(argv[2])

    staticelo.controller.calc.rating(season=season, K=K, XI=400.0)


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    main(argc, argv)