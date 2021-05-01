from enum import Enum
from functools import partial
from typing import List

if __name__ == '__main__':
    from puzzle import Puzzle
else:
    from .puzzle import Puzzle


def set_value(arr: List[int], x: int, y: int, value: int, size: int):
    arr[size * y + x] = value


def snake(size: int, left: bool, top: bool, direction: bool) -> Puzzle:
    if direction:
        arr = list(range(1, size ** 2 + 1))
        print(arr, left, top, direction)
        if not top:
            arr = arr[::-1]
        for i in range(size):
            if ((i % 2) == (size % 2)) is not (left and top):
                arr[i * size:(i + 1) * size] = arr[i * size:(i + 1) * size][::-1]
    else:
        arr = []
        for i in range(1, size + 1):
            arr.extend(list(range(i, size ** 2 + 1, size)))
        print(arr, left, top, direction)
        if not left:
            arr = arr[::-1]
        for i in range(size):
            if ((i % 2) == (size % 2)) is not (left and top):
                arr[i:size * size:size] = arr[i:size * size:size][::-1]
    arr[arr.index(size ** 2)] = 0
    print(arr, left, top, direction)
    return arr, 0, None


def spiral(size: int, left: bool, top: bool, direction: bool) -> Puzzle:
    arr = [0 for _ in range(size ** 2)]



    return arr, 0, None


def direct(size: int, left: bool, top: bool, direction: bool) -> Puzzle:
    arr = [0 for _ in range(size ** 2)]

    return arr, 0, None


class FinalPuzzle(Enum):
    snake_top_left_to_right = partial(snake, left=True, top=True, direction=True)
    snake_top_left_to_bottom = partial(snake, left=True, top=True, direction=False)
    snake_top_right_to_left = partial(snake, left=False, top=True, direction=True)
    snake_top_right_to_bottom = partial(snake, left=False, top=True, direction=False)
    snake_bottom_left_to_right = partial(snake, left=True, top=False, direction=True)
    snake_bottom_left_to_top = partial(snake, left=True, top=False, direction=False)
    snake_bottom_right_to_left = partial(snake, left=False, top=False, direction=True)
    snake_bottom_right_to_top = partial(snake, left=False, top=False, direction=False)

    spiral_top_left_to_right = partial(spiral, left=True, top=True, direction=True)
    spiral_top_left_to_bottom = partial(spiral, left=True, top=True, direction=False)
    spiral_top_right_to_left = partial(spiral, left=False, top=True, direction=True)
    spiral_top_right_to_bottom = partial(spiral, left=False, top=True, direction=False)
    spiral_bottom_left_to_right = partial(spiral, left=True, top=False, direction=True)
    spiral_bottom_left_to_top = partial(spiral, left=True, top=False, direction=False)
    spiral_bottom_right_to_left = partial(spiral, left=False, top=False, direction=True)
    spiral_bottom_right_to_top = partial(spiral, left=False, top=False, direction=False)

    direct_top_left_to_right = partial(direct, left=True, top=True, direction=True)
    direct_top_left_to_bottom = partial(direct, left=True, top=True, direction=False)
    direct_top_right_to_left = partial(direct, left=False, top=True, direction=True)
    direct_top_right_to_bottom = partial(direct, left=False, top=True, direction=False)
    direct_bottom_left_to_right = partial(direct, left=True, top=False, direction=True)
    direct_bottom_left_to_top = partial(direct, left=True, top=False, direction=False)
    direct_bottom_right_to_left = partial(direct, left=False, top=False, direction=True)
    direct_bottom_right_to_top = partial(direct, left=False, top=False, direction=False)

    def __call__(self, *args, **kwargs):
        return self.value(*args)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_string(s: str) -> str:
        try:
            return FinalPuzzle[s]
        except KeyError:
            raise ValueError


def main():
    from puzzle_solver import PuzzleSolver
    print(PuzzleSolver.print(snake(3, left=True, top=True, direction=True)[0], 3))
    print(PuzzleSolver.print(snake(3, left=True, top=True, direction=False)[0], 3))
    print(PuzzleSolver.print(snake(3, left=False, top=True, direction=True)[0], 3))
    print(PuzzleSolver.print(snake(3, left=False, top=True, direction=False)[0], 3))
    print(PuzzleSolver.print(snake(3, left=True, top=False, direction=True)[0], 3))
    print(PuzzleSolver.print(snake(3, left=True, top=False, direction=False)[0], 3))
    print(PuzzleSolver.print(snake(3, left=False, top=False, direction=True)[0], 3))
    print(PuzzleSolver.print(snake(3, left=False, top=False, direction=False)[0], 3))


if __name__ == '__main__':
    main()
