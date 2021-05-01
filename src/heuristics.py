from collections import defaultdict
from enum import Enum
from functools import partial
from math import sqrt

if __name__ == 'heuristics':
    from puzzle import Puzzle
else:
    from .puzzle import Puzzle


def uniform(*unused) -> float:
    return 0


def hamming(puzzle: Puzzle, final_puzzle: Puzzle, *unused) -> float:
    return sum(1 for elem1, elem2 in zip(puzzle[0], final_puzzle[0]) if elem1 != elem2 and elem1 != 0)


def manhattan(puzzle: Puzzle, final_puzzle: Puzzle, size: int) -> float:
    final_arr = final_puzzle[0]
    return sum(
        abs(i // size - final_arr.index(elem) // size) + abs(i % size - final_arr.index(elem) % size)
        for i, elem in enumerate(puzzle[0]) if elem != 0
    )


def euclidean(puzzle: Puzzle, final_puzzle: Puzzle, size: int) -> float:
    final_arr = final_puzzle[0]
    return sum(
        sqrt(abs(i // size - final_arr.index(elem) // size) ** 2 + abs(i % size - final_arr.index(elem) % size) ** 2)
        for i, elem in enumerate(puzzle[0]) if elem != 0
    )


def linear_conflict(puzzle: Puzzle, final_puzzle: Puzzle, size: int) -> float:
    md = manhattan(puzzle, final_puzzle, size)
    lc = 0
    for row in range(size):
        elems = set(puzzle[0][row * size:row * (size + 1)]) & set(final_puzzle[0][row * size:row * (size + 1)])
        indices = sorted((puzzle[0].index(elem), final_puzzle[0].index(elem)) for elem in elems)
        dct = defaultdict(list)
        for i, (index_1, final_index_1) in enumerate(indices):
            for (index_2, final_index_2) in indices[i + 1:]:
                if final_index_2 < final_index_1:
                    dct[index_1].append(index_2)
    for column in range(size):
        dct = {}

    lc *= 2
    return md + lc


class Heuristic(Enum):
    uniform = partial(uniform)
    hamming = partial(hamming)
    manhattan = partial(manhattan)
    euclidean = partial(euclidean)
    linear_conflict = partial(linear_conflict)

    def __call__(self, *args, **kwargs):
        return self.value(*args)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_string(s: str) -> str:
        try:
            return Heuristic[s]
        except KeyError:
            raise ValueError
