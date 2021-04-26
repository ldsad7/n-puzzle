import dataclasses
from typing import List, Optional, Generator, Set


@dataclasses.dataclass
class Puzzle:
    arr: List[int]
    size: int
    prev_puzzle: Optional['Puzzle']
    cost: int

    def __lt__(self, other: 'Puzzle'):
        if self.size != other.size:
            return self.size < other.size
        return self.cost < other.cost

    def __eq__(self, other: 'Puzzle'):
        return self.size == other.size and self.arr == other.arr

    def __le__(self, other: 'Puzzle'):
        return self.__lt__(other) or self.__eq__(other)

    def __hash__(self):
        return hash((self.size, tuple(self.arr)))

    def __iter__(self):
        return iter(self.arr)

    def __str__(self):
        width = len(str(self.size * self.size))
        result = ''
        for i in range(self.size):
            for j in range(self.size - 1):
                result += str(self.arr[i + j * self.size]).rjust(width) + ' '
            result += str(self.arr[i + (self.size - 1) * self.size]).rjust(width) + '\n'
        return result.strip()

    def get_adjacent_puzzles(self) -> Set['Puzzle']:
        index = self.arr.index(0)
        directions = []
        if index % self.size > 0:  # left
            directions.append(index - 1)
        if index % self.size < self.size - 1:  # right
            directions.append(index + 1)
        if index / self.size > 0:  # up
            directions.append(index - self.size)
        if index / self.size < self.size - 1:  # down
            directions.append(index + self.size)
        puzzles = set()
        for direction in directions:
            new_arr = self.arr[:]
            new_arr[index] = self.arr[direction]
            new_arr[direction] = 0
            puzzles.add(Puzzle(new_arr, self.size, self, self.cost + 1))
        return puzzles
