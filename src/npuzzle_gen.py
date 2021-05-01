import argparse
import random
from typing import List, Tuple

if __name__ == '__main__':
    from puzzle_solver import PuzzleSolver
else:
    from .puzzle_solver import PuzzleSolver


def swap_empty(p: List[int], size: int) -> None:
    idx = p.index(0)
    directions = []
    if (idx % size) > 0:  # left
        directions.append(idx - 1)
    if (idx % size) < (size - 1):  # right
        directions.append(idx + 1)
    if (idx // size) > 0:  # up
        directions.append(idx - size)
    if (idx // size) < (size - 1):  # down
        directions.append(idx + size)
    swi = random.choice(directions)
    p[idx] = p[swi]
    p[swi] = 0


def make_puzzle(size: int, solvable: bool, iterations: int) -> Tuple[int, ...]:
    arr = make_start_arr(size)
    for _ in range(iterations):
        swap_empty(arr, size)
    if not solvable:
        if (arr[0] == 0) or (arr[1] == 0):
            arr[2], arr[3] = arr[3], arr[2]
        else:
            arr[0], arr[1] = arr[1], arr[0]
    return tuple(arr)


def make_start_arr(size: int) -> List[int]:
    return list(range(1, size ** 2)) + [0]


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
    parser.add_argument("-i", "--iterations", type=int, default=50000, help="Number of passes")
    args = parser.parse_args()

    random.seed()

    puzzle: Tuple[int, ...] = make_puzzle(args.size, solvable=args.solvable, iterations=args.iterations)

    print(f"# This puzzle is {'solvable' if args.solvable else 'unsolvable'}")
    print(args.size)
    PuzzleSolver.print(puzzle, args.size)
