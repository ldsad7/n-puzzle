import heapq
from typing import List, Dict, Tuple, Set

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

    def solve(self, puzzle: Puzzle) -> None:
        if self.is_solvable(puzzle):
            self.a_star(puzzle)
        else:
            print(f'Puzzle\n')
            print(puzzle[0], self.size)
            print('\nis not solvable')

    @staticmethod
    def print(arr: Tuple[int], size: int) -> None:
        width = len(str(size ** 2))
        for i in range(size):
            for j in range(size - 1):
                print(str(arr[j + i * size]).rjust(width), end=' ')
            print(str(arr[size - 1 + i * size]).rjust(width))

    def print_full_path(self, puzzle: Puzzle, complexity_in_time: int, complexity_in_size: int) -> None:
        path: List[Tuple[int]] = []
        while puzzle is not None:
            path.append(puzzle[0])
            puzzle = puzzle[2]
        self.print(path[-1], self.size)
        for arr in path[-2::-1]:
            print('>')
            self.print(arr, self.size)
        print(f'Complexity in time: {complexity_in_time}')
        print(f'Complexity in size: {complexity_in_size}')
        print(f'Steps: {len(path) - 1}')

    def get_adjacent_arrays(self, arr: Tuple[int]) -> Set[Tuple[int]]:
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

    def a_star(self, puzzle: Puzzle) -> None:
        # TODO: let users send final_puzzle here
        final_puzzle: Puzzle = (tuple(list(range(1, self.size ** 2)) + [0]), 0, None)
        open_set: Dict[Tuple[int], Tuple[int, float]] = {
            puzzle[0]: (puzzle[1], self.heuristic(puzzle, final_puzzle, self.size))
        }
        queue: List[Tuple[float, Puzzle]] = [(sum(open_set[puzzle[0]]), puzzle)]
        closed_set: Set[Tuple[int]] = set()
        while queue:
            _, node_puzzle = heapq.heappop(queue)
            if node_puzzle[0] == final_puzzle[0]:
                return self.print_full_path(
                    node_puzzle, complexity_in_time=len(open_set), complexity_in_size=len(closed_set)
                )
            closed_set.add(node_puzzle[0])
            for new_arr in self.get_adjacent_arrays(node_puzzle[0]) - closed_set:
                if new_arr not in open_set:
                    new_puzzle = (new_arr, node_puzzle[1] + self.step, node_puzzle)
                    open_set[new_arr] = (new_puzzle[1], self.heuristic(new_puzzle, final_puzzle, self.size))
                    heapq.heappush(queue, (sum(open_set[new_arr]), new_puzzle))
                elif (node_puzzle[1] + self.step) < open_set[new_arr][0]:
                    open_set[new_arr] = (node_puzzle[1] + self.step, open_set[new_arr][1])
                    new_puzzle = (new_arr, open_set[new_arr][0], node_puzzle)
                    heapq.heappush(queue, (sum(open_set[new_arr]), new_puzzle))
