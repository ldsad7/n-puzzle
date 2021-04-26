from enum import Enum
from functools import partial

from puzzle import Puzzle


def hamming(puzzle: Puzzle, final_puzzle: Puzzle) -> float:
    return sum(1 for elem1, elem2 in zip(puzzle, final_puzzle) if elem1 != elem2)


def manhattan(puzzle: Puzzle, final_puzzle: Puzzle) -> float:
    return 1


def euclidean(puzzle: Puzzle, final_puzzle: Puzzle) -> float:
    return 1


def linear_conflict(puzzle: Puzzle, final_puzzle: Puzzle) -> float:
    return 1


class Heuristic(Enum):
    hamming = partial(hamming)
    manhattan = partial(hamming)
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
