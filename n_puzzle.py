import argparse
import traceback
from typing import Optional

from heuristic import Heuristic
from puzzle import Puzzle
from puzzle_reader import PuzzleReader
from puzzle_solver import PuzzleSolver


def main(path: Optional[str], size: Optional[int], heuristic: Heuristic = Heuristic.manhattan, verbose: bool = False):
    puzzle_reader: PuzzleReader = PuzzleReader(verbose)
    puzzle: Puzzle = puzzle_reader.read(path, size)
    puzzle_solver: PuzzleSolver = PuzzleSolver(heuristic, verbose)
    puzzle_solver.solve(puzzle)
    puzzle_solver.print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='N-puzzle solver')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--path', type=str, help='path to the file with n-puzzle')
    group.add_argument('-s', '--size', type=int, help='size of generated n-puzzle')
    parser.add_argument(
        '-f', '--heuristic', type=Heuristic.from_string, choices=list(Heuristic), default=Heuristic.manhattan
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='подробный вывод')
    args = parser.parse_args()
    try:
        main(args.path, args.size, args.heuristic, args.verbose)
    except Exception as e:
        traceback.print_exc()
        print(f'Произошла ошибка: {e}')
