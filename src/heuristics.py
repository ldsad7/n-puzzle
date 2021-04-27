from enum import Enum
from functools import partial
from math import sqrt

from .puzzle import Puzzle


def uniform(*unused) -> float:
    return 0


def hamming(puzzle: Puzzle, final_puzzle: Puzzle, *unused) -> float:
    return sum(1 for elem1, elem2 in zip(puzzle[0], final_puzzle[0]) if elem1 != elem2)


def manhattan(puzzle: Puzzle, final_puzzle: Puzzle, size: int) -> float:
    final_arr = final_puzzle[0]
    return sum(
        abs(i // size - final_arr.index(elem) // size) + abs(i % size - final_arr.index(elem) % size)
        for i, elem in enumerate(puzzle[0])
    )


def euclidean(puzzle: Puzzle, final_puzzle: Puzzle, size: int) -> float:
    final_arr = final_puzzle[0]
    return sum(
        sqrt(
            abs(i // size - final_arr.index(elem) // size) ** 2 + abs(i % size - final_arr.index(elem) % size) ** 2
        )
        for i, elem in enumerate(puzzle[0])
    )


def linear_conflict(puzzle: Puzzle, final_puzzle: Puzzle) -> float:
    return 1


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
