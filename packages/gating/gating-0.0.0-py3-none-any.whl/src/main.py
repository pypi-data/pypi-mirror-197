import argparse
from src.gating import gating


def main():
    parser = argparse.ArgumentParser(prog='gating', description='Code to perform gating in data from csv tables')
    parser.add_argument('--path', '-p', required=True, type=str, help='path to the csv file to generate gate')
    parser.add_argument('--path_to_save', '-ps', required=True, type=str,
                        help='path to save csv with cells in the gate')
    parser.add_argument('-x', required=False, type=str, help='name of column to plot in the X axis', default="X")
    parser.add_argument('-y', required=False, type=str, help='name of column to plot in the Y axis', default="Y")

    args = parser.parse_args()

    gating(args.path, args.path_to_save, args.x, args.y)

    return


if __name__ == '__main__':
    main()
