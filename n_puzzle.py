import argparse
from typing import Optional

from src import PuzzleReader, PuzzleSolver, Heuristic


def main(path: Optional[str], size: Optional[int], heuristic: Heuristic = Heuristic.manhattan,
         greedy: bool = False, verbose: bool = False):
    puzzle_reader: PuzzleReader = PuzzleReader(verbose)
    puzzle, size = puzzle_reader.read(path, size)
    puzzle_solver: PuzzleSolver = PuzzleSolver(size, heuristic, greedy, verbose)
    puzzle_solver.solve(puzzle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='N-puzzle solver')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--path', type=str, help='path to the file with n-puzzle')
    group.add_argument('-s', '--size', type=int, help='size of generated n-puzzle')
    parser.add_argument(
        '-f', '--heuristic', type=Heuristic.from_string, choices=list(Heuristic), default=Heuristic.manhattan
    )
    parser.add_argument('-g', '--greedy', action='store_true', default=False, help='is greedy search')
    parser.add_argument('-u', '--uniform', action='store_true', default=False, help='is uniform search')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    try:
        main(args.path, args.size, args.heuristic, args.greedy, args.verbose)
    except Exception as e:
        # TODO: remove later
        import traceback

        traceback.print_exc()
        print(f'Произошла ошибка: {e}')
