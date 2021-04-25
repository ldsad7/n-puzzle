import argparse
import random


def swap_empty(p, size):
    idx = p.index(0)
    directions = []
    if idx % size > 0:  # left
        directions.append(idx - 1)
    if idx % size < size - 1:  # right
        directions.append(idx + 1)
    if idx / size > 0:  # up
        directions.append(idx - size)
    if idx / size < size - 1:  # down
        directions.append(idx + size)
    swi = random.choice(directions)
    p[idx] = p[swi]
    p[swi] = 0


def make_puzzle(size, solvable, iterations):
    arr = make_start_arr(size)
    for _ in range(iterations):
        swap_empty(arr, size)
    if not solvable:
        if arr[0] == 0 or arr[1] == 0:
            arr[2], arr[3] = arr[3], arr[2]
        else:
            arr[0], arr[1] = arr[1], arr[0]
    return arr


def make_start_arr(size):
    arr = [0 for _ in range(size * size)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while cur < size * size:
        arr[x + y * size] = cur
        if x + ix == size or x + ix < 0 or (ix != 0 and arr[x + ix + y * size] != 0):
            iy = ix
            ix = 0
        elif y + iy == size or y + iy < 0 or (iy != 0 and arr[x + (y + iy) * size] != 0):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        cur += 1
    return arr


class SizeAction(argparse.Action):
    def __call__(self, parser_, namespace, value, option_string=None):
        if value < 2:
            parser_.error("Can't generate a puzzle with size lower than 2. It says so in the help. Dummy.")
        setattr(namespace, self.dest, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("size", type=int, action=SizeAction, help="Size of the puzzle's side. Must be >= 2.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--solvable", action="store_true", default=False,
                       help="Forces generation of a solvable puzzle")
    group.add_argument("-u", "--unsolvable", action="store_true", default=False,
                       help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")
    args = parser.parse_args()

    random.seed()

    puzzle = make_puzzle(args.size, solvable=args.solvable, iterations=args.iterations)

    width = len(str(args.size * args.size))
    print(f"# This puzzle is {'solvable' if args.solvable else 'unsolvable'}")
    print(args.size)
    for i in range(args.size):
        for j in range(args.size - 1):
            print(str(puzzle[i + j * args.size]).rjust(width), end=' ')
        print(str(puzzle[i + (args.size - 1) * args.size]).rjust(width))
