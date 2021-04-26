import heapq
from typing import Optional, List, Dict

from heuristic import Heuristic
from puzzle import Puzzle


class PuzzleSolver:
    def __init__(self, heuristic: Heuristic = Heuristic.manhattan, verbose: bool = False):
        self.heuristic = heuristic
        self.verbose = verbose

    def solve(self, puzzle: Puzzle) -> None:
        # TODO: check that puzzle is solvable
        self.a_star(puzzle)

    def print(self) -> None:
        pass

    def print_full_path(self, puzzle: Optional[Puzzle]) -> None:
        path = []
        while puzzle is not None:
            path.append(puzzle)
            puzzle = puzzle.prev_puzzle
        if path:
            print(path[-1])
            for puzzle in path[-2::-1]:
                print(f'>\n{puzzle}')
        print(f'Complexity in time {1}')
        print(f'Complexity in size {1}')
        print(f'Steps: {puzzle.size}')

    def a_star(self, puzzle: Puzzle) -> None:
        # TODO: let users send final_puzzle here
        final_puzzle: Puzzle = Puzzle(
            arr=list(range(1, puzzle.size * puzzle.size)) + [0], size=puzzle.size, prev_puzzle=None, cost=0
        )
        # NB: queue and open_set have the same ref for array
        open_set: Dict[Puzzle, List[float, Puzzle]] = {
            puzzle: [puzzle.cost + self.heuristic(puzzle, final_puzzle), puzzle]
        }
        queue: List[List[float, Puzzle]] = [open_set[puzzle]]
        closed_set = set()
        while queue:
            _, node_puzzle = heapq.heappop(queue)
            if node_puzzle == final_puzzle:
                self.print_full_path(node_puzzle)
                return
            closed_set.add(node_puzzle)
            for new_puzzle in node_puzzle.get_adjacent_puzzles() - closed_set:
                if new_puzzle in open_set:
                    _, prev_puzzle = open_set[new_puzzle]
                    if new_puzzle.cost < prev_puzzle.cost:
                        open_set[new_puzzle][0] = open_set[new_puzzle][0] - prev_puzzle.cost + new_puzzle.cost
                        prev_puzzle.cost = new_puzzle.cost
                        prev_puzzle.prev_puzzle = new_puzzle.prev_puzzle

                        # restoring PriorityQueue after changing priority number...
                        index = queue.index(open_set[new_puzzle])
                        while index > 0:
                            if queue[index][0] >= queue[(index - 1) // 2][0]:
                                break
                            queue[index], queue[(index - 1) // 2] = queue[(index - 1) // 2], queue[index]
                            index = (index - 1) // 2
                else:
                    open_set[new_puzzle] = [new_puzzle.cost + self.heuristic(new_puzzle, final_puzzle), new_puzzle]
                    heapq.heappush(queue, open_set[new_puzzle])
