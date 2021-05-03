import heapq
import time
from typing import List, Dict, Tuple, Set

if __name__ == 'puzzle_solver':
    from heuristics import Heuristic
    from puzzle import Puzzle
else:
    from .heuristics import Heuristic
    from .puzzle import Puzzle


class Colors:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PINK = '\033[95m'
    CYAN = '\033[96m'


class PuzzleSolver:
    def __init__(self, size: int, heuristic: Heuristic = Heuristic.manhattan,
                 greedy: bool = False, verbose: bool = False, visualization: bool = False):
        self.size = size
        self.heuristic = heuristic
        self.step = 0 if greedy else 1
        self.verbose = verbose
        self.visualization = visualization

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
            print(f'{Colors.BOLD}Puzzle{Colors.ENDC}{Colors.CYAN}')
            self.print(puzzle[0], puzzle_size)
            print(f'{Colors.ENDC}{Colors.BOLD}is not solvable into{Colors.ENDC}{Colors.GREEN}')
            self.print(final_puzzle[0], final_puzzle_size)
            print(Colors.ENDC, end='')

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
        if self.visualization:
            moves_arr = []
            for i in range(len(path) - 1, 0, -1):
                moves_arr.append((path[i].index(0), path[i - 1].index(0)))
            print(f'size = {self.size}\n'
                  f'startIntArray = {list(path[-1])}\n'
                  f'finalIntArray = {list(path[0])}\n'
                  f'let inputMovesArray = {moves_arr}')
        else:
            print(f'{Colors.CYAN}greedy search{Colors.ENDC}: '
                  f'{Colors.RED + "NO" if self.step else Colors.GREEN + "YES"}{Colors.ENDC}')
            print(f'{Colors.CYAN}uniform cost search{Colors.ENDC}: '
                  f'{Colors.GREEN + "YES" if self.heuristic == Heuristic.uniform else Colors.RED + "NO"}{Colors.ENDC}')
            print(f'{Colors.CYAN}solvable{Colors.ENDC}: {Colors.GREEN}YES{Colors.ENDC}')
            print(f'{Colors.YELLOW}heuristic function{Colors.ENDC}: {Colors.GREEN}{self.heuristic.name}{Colors.ENDC}')
            print(f'{Colors.CYAN}puzzle size{Colors.ENDC}: {Colors.GREEN}{self.size}{Colors.ENDC}')
            print(f'{Colors.CYAN}initial state{Colors.ENDC}: {Colors.GREEN}{path[-1]}{Colors.ENDC}')
            print(f'{Colors.CYAN}final state{Colors.ENDC}: {Colors.GREEN}{path[0]}{Colors.ENDC}')
            print(f'{Colors.YELLOW}heuristic score for initial state:{Colors.ENDC}')
            for heuristic in list(Heuristic):
                print(f'\t- {Colors.PINK}{heuristic.name}{Colors.ENDC}: '
                      f'{Colors.BOLD}{heuristic(path[-1], path[0], self.size)}{Colors.ENDC}')
            print(f'{Colors.RED}search algorithm{Colors.ENDC}: {Colors.BLUE}A*{Colors.ENDC}')
            print(f'{Colors.BOLD}solution{Colors.ENDC}: {Colors.CYAN}')
            self.print(path[-1], self.size)
            print(Colors.ENDC, end='')
            for arr in path[-2::-1]:
                print(f'{Colors.BOLD}>{Colors.ENDC}{Colors.CYAN}')
                self.print(arr, self.size)
                print(Colors.ENDC, end='')
            print(f'{Colors.YELLOW}Complexity in time{Colors.ENDC}: {Colors.PINK}{complexity_in_time}{Colors.ENDC}')
            print(f'{Colors.YELLOW}Complexity in size{Colors.ENDC}: {Colors.PINK}{complexity_in_size}{Colors.ENDC}')
            print(f'{Colors.YELLOW}Steps{Colors.ENDC}: {Colors.PINK}{len(path) - 1}{Colors.ENDC}')
            print(f'{Colors.YELLOW}Passed time{Colors.ENDC}: {Colors.PINK}{passed_time} sec{Colors.ENDC}')

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
                print(f'{Colors.YELLOW}Current puzzle{Colors.ENDC}: {Colors.PINK}{node_puzzle[0]}{Colors.ENDC}, '
                      f'{Colors.YELLOW}complexity_in_time{Colors.ENDC}: {Colors.PINK}{len(open_set)}{Colors.ENDC}, '
                      f'{Colors.YELLOW}complexity_in_size{Colors.ENDC}: {Colors.PINK}{len(closed_set)}{Colors.ENDC}')
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
        raise ValueError(f"We weren't able to solve the puzzle {puzzle[0]} somehow...")
