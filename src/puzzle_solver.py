import heapq
import time
from typing import List, Dict, Tuple, Set

if __name__ == 'puzzle_solver':
    from heuristics import Heuristic
    from puzzle import Puzzle
else:
    from .heuristics import Heuristic
    from .puzzle import Puzzle


class PuzzleSolver:
    def __init__(self, size: int, heuristic: Heuristic = Heuristic.manhattan,
                 greedy: bool = False, verbose: bool = False):
        self.size = size
        self.heuristic = heuristic
        self.step = 0 if greedy else 1
        self.verbose = verbose

    def is_solvable(self, puzzle: Puzzle):
        num_of_inversions = 0
        processed_set = set()
        for elem in puzzle[0]:
            num_of_inversions += len(set(range(1, elem)) - processed_set)
            processed_set.add(elem)
        if (self.size % 2) == 0:
            return ((num_of_inversions + 1 + (puzzle[0].index(0) // self.size)) % 2) == 0
        return (num_of_inversions % 2) == 0

    def solve(self, puzzle: Puzzle, final_puzzle: Puzzle, puzzle_size: int, final_puzzle_size: int) -> None:
        if puzzle_size == final_puzzle_size and self.is_solvable(puzzle) == self.is_solvable(final_puzzle):
            self.a_star(puzzle, final_puzzle)
        else:
            print(f'Puzzle')
            self.print(puzzle[0], puzzle_size)
            print('is not solvable into')
            self.print(final_puzzle[0], final_puzzle_size)

    @staticmethod
    def print(arr: Tuple[int, ...], size: int) -> None:
        width = len(str(size ** 2))
        for i in range(size):
            for j in range(size - 1):
                print(str(arr[j + i * size]).rjust(width), end=' ')
            print(str(arr[size - 1 + i * size]).rjust(width))

    def print_full_path(self, puzzle: Puzzle, complexity_in_time: int, complexity_in_size: int,
                        passed_time: float) -> None:
        path: List[Tuple[int, ...]] = []
        while puzzle is not None:
            path.append(puzzle[0])
            puzzle = puzzle[2]
        self.print(path[-1], self.size)
        for arr in path[-2::-1]:
            print('>')
            self.print(arr, self.size)
        print(f'Complexity in time: {complexity_in_time}\nComplexity in size: {complexity_in_size}\n'
              f'Steps: {len(path) - 1}\nPassed time: {passed_time} sec')

    def get_adjacent_arrays(self, arr: Tuple[int, ...]) -> Set[Tuple[int, ...]]:
        index = arr.index(0)
        directions = []
        if (index % self.size) > 0:  # left
            directions.append(index - 1)
        if (index % self.size) < (self.size - 1):  # right
            directions.append(index + 1)
        if (index // self.size) > 0:  # up
            directions.append(index - self.size)
        if (index // self.size) < (self.size - 1):  # down
            directions.append(index + self.size)
        puzzles = set()
        for direction in directions:
            new_arr = list(arr)
            new_arr[index] = arr[direction]
            new_arr[direction] = 0
            puzzles.add(tuple(new_arr))
        return puzzles

    def a_star(self, puzzle: Puzzle, final_puzzle: Puzzle) -> None:
        start_time = time.time()
        final_arr: Tuple[int, ...] = final_puzzle[0]
        open_set: Dict[Tuple[int], Tuple[float, float]] = {
            puzzle[0]: (puzzle[1], self.heuristic(puzzle[0], final_arr, self.size))
        }
        closed_set: Set[Tuple[int, ...]] = set()
        queue: List[Tuple[float, Puzzle]] = [(sum(open_set[puzzle[0]]), puzzle)]
        while queue:
            _, node_puzzle = heapq.heappop(queue)
            if self.verbose:
                print(f'Current puzzle: {node_puzzle[0]}, complexity_in_time: {len(open_set)}, '
                      f'complexity_in_size: {len(closed_set)}')
            closed_set.add(node_puzzle[0])
            if node_puzzle[0] == final_arr:
                return self.print_full_path(
                    node_puzzle, complexity_in_time=len(open_set), complexity_in_size=len(closed_set),
                    passed_time=time.time() - start_time
                )
            for new_arr in self.get_adjacent_arrays(node_puzzle[0]) - closed_set:
                if new_arr not in open_set:
                    new_puzzle = (new_arr, self.step + node_puzzle[1], node_puzzle)
                    open_set[new_arr] = (new_puzzle[1], self.heuristic(new_puzzle[0], final_arr, self.size))
                    heapq.heappush(queue, (sum(open_set[new_arr]), new_puzzle))
                elif (self.step + node_puzzle[1]) < open_set[new_arr][0]:
                    open_set[new_arr] = (self.step + node_puzzle[1], open_set[new_arr][1])
                    new_puzzle = (new_arr, open_set[new_arr][0], node_puzzle)
                    heapq.heappush(queue, (sum(open_set[new_arr]), new_puzzle))
        raise ValueError("Не смогли решить puzzle")
