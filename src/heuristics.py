from collections import defaultdict
from enum import Enum
from functools import partial
from math import sqrt
from typing import Tuple, Set, List


def uniform(*_) -> float:
    return 0


def hamming(arr: Tuple[int, ...], final_arr: Tuple[int, ...], _: int) -> float:
    return sum(1 for elem1, elem2 in zip(arr, final_arr) if elem1 != elem2 and elem1 != 0)


def gaschnig(arr: Tuple[int, ...], final_arr: Tuple[int, ...], size: int) -> float:
    count = 0
    list_arr: List[int] = list(arr)
    final_list_arr: List[int] = list(final_arr)
    while list_arr != final_list_arr:
        index_1 = list_arr.index(0)
        index_2 = list_arr.index(final_list_arr[index_1])
        if index_1 == index_2:
            i = 0
            for i in range(size * size):
                if list_arr[size * size - 1 - i] != final_list_arr[size * size - 1 - i]:
                    break
            list_arr[index_1], list_arr[size * size - 1 - i] = list_arr[size * size - 1 - i], list_arr[index_1]
        else:
            list_arr[index_1], list_arr[index_2] = list_arr[index_2], list_arr[index_1]
        count += 1
    return count


def manhattan(arr: Tuple[int, ...], final_arr: Tuple[int, ...], size: int) -> float:
    return sum(
        abs(i // size - final_arr.index(elem) // size) + abs(i % size - final_arr.index(elem) % size)
        for i, elem in enumerate(arr) if elem != 0
    )


def euclidean(arr: Tuple[int, ...], final_arr: Tuple[int, ...], size: int) -> float:
    return sum(
        sqrt((i // size - final_arr.index(elem) // size) ** 2 + (i % size - final_arr.index(elem) % size) ** 2)
        for i, elem in enumerate(arr) if elem != 0
    )


def linear_conflict(arr: Tuple[int, ...], final_arr: Tuple[int, ...], size: int) -> float:
    def count_lc(elems: Set[int]) -> int:
        inner_lc = 0
        indices = sorted((arr.index(elem), final_arr.index(elem)) for elem in elems)
        dct = defaultdict(set)
        for i, (index_1, final_index_1) in enumerate(indices):
            for (index_2, final_index_2) in indices[i + 1:]:
                if final_index_2 < final_index_1:
                    dct[index_1].add(index_2)
                    dct[index_2].add(index_1)
        while dct:
            index: int = max(dct.items(), key=lambda elem: len(elem[1]))[0]
            for inner_index in dct[index]:
                dct[inner_index].remove(index)
            del dct[index]
            inner_lc += 2
        return inner_lc

    lc = 0
    for row in range(size):
        lc += count_lc(set(arr[row * size:(row + 1) * size]) & set(final_arr[row * size:(row + 1) * size]) - {0})
    for column in range(size):
        lc += count_lc(set(arr[column::size]) & set(final_arr[column::size]) - {0})
    md = manhattan(arr, final_arr, size)
    return md + lc


class Heuristic(Enum):
    uniform = partial(uniform)
    hamming = partial(hamming)
    gaschnig = partial(gaschnig)
    euclidean = partial(euclidean)
    manhattan = partial(manhattan)

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
