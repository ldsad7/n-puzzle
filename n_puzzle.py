import argparse
from typing import Optional

from src import PuzzleReader, PuzzleSolver, Heuristic, FinalPuzzle


def main(path: Optional[str], result_path: Optional[str], size: Optional[int],
         heuristic: Heuristic = Heuristic.manhattan,
         final_puzzle_func: FinalPuzzle = FinalPuzzle.direct_top_left_to_right, greedy: bool = False,
         verbose: bool = False):
    puzzle_reader: PuzzleReader = PuzzleReader(verbose)
    puzzle, puzzle_size = puzzle_reader.read(path, size)
    puzzle_solver: PuzzleSolver = PuzzleSolver(puzzle_size, heuristic, greedy, verbose)
    if result_path is not None:
        final_puzzle, final_puzzle_size = puzzle_reader.read(result_path, size)
    else:
        final_puzzle = final_puzzle_func(puzzle_size)
        final_puzzle_size = puzzle_size
    puzzle_solver.solve(puzzle, final_puzzle, puzzle_size, final_puzzle_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='N-puzzle solver')
    group_1 = parser.add_mutually_exclusive_group(required=True)
    group_1.add_argument('-p', '--path', type=str, help='path to the file with start n-puzzle')
    group_1.add_argument('-s', '--size', type=int, help='size of generated n-puzzle')
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument('--result_path', type=str, help='path to the file with final n-puzzle')
    group_2.add_argument(
        '-r', '--result', type=FinalPuzzle.from_string, choices=list(FinalPuzzle),
        default=FinalPuzzle.direct_top_left_to_right
    )
    parser.add_argument(
        '-f', '--heuristic', type=Heuristic.from_string, choices=list(Heuristic), default=Heuristic.manhattan,
        help='heuristic to use'
    )
    parser.add_argument('-g', '--greedy', action='store_true', default=False, help='is greedy search')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()
    try:
        main(args.path, args.result_path, args.size, args.heuristic, args.result, args.greedy, args.verbose)
    except Exception as e:
        print(f'Произошла ошибка: {e}')
