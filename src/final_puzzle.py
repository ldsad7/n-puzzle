from enum import Enum
from functools import partial

if __name__ == '__main__':
    from puzzle import Puzzle
else:
    from .puzzle import Puzzle


def snake(size: int, left: bool, top: bool, direction: bool) -> Puzzle:
    if direction:
        arr = list(range(1, size ** 2 + 1))

        if not top:
            arr = arr[::-1]

        for i in range(size):
            if top:
                if left and (i % 2 == 1):
                    arr[i * size:(i + 1) * size] = arr[i * size:(i + 1) * size][::-1]
                elif not left and (i % 2 == 0):
                    arr[i * size:(i + 1) * size] = arr[i * size:(i + 1) * size][::-1]
            else:
                if left and ((i % 2) == ((size - 1) % 2)):
                    arr[i * size:(i + 1) * size] = arr[i * size:(i + 1) * size][::-1]
                elif not left and ((i % 2) == (size % 2)):
                    arr[i * size:(i + 1) * size] = arr[i * size:(i + 1) * size][::-1]
    else:
        arr = []
        for i in range(1, size + 1):
            arr.extend(list(range(i, size ** 2 + 1, size)))

        if not left:
            arr = arr[::-1]

        for i in range(size):
            if left:
                if top and (i % 2 == 1):
                    arr[i:size * size:size] = arr[i:size * size:size][::-1]
                elif not top and (i % 2 == 0):
                    arr[i:size * size:size] = arr[i:size * size:size][::-1]
            else:
                if top and ((i % 2) == ((size - 1) % 2)):
                    arr[i:size * size:size] = arr[i:size * size:size][::-1]
                elif not top and ((i % 2) == (size % 2)):
                    arr[i:size * size:size] = arr[i:size * size:size][::-1]

    arr[arr.index(size ** 2)] = 0
    return arr, 0, None


def spiral(size: int, left: bool, top: bool, direction: bool) -> Puzzle:
    arr = [0 for _ in range(size ** 2)]

    left_max = 0
    right_max = size - 1
    top_max = 0
    bottom_max = size - 1

    x = 0 if left else size - 1
    y = 0 if top else size - 1

    if direction:
        if left and top:
            dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            top_max = 1
        elif left and not top:
            dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
            bottom_max = size - 2
        elif not left and top:
            dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            top_max = 1
        else:
            dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            bottom_max = size - 2
    else:
        if left and top:
            dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            left_max = 1
        elif left and not top:
            dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            left_max = 1
        elif not left and top:
            dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
            right_max = size - 2
        else:
            dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            right_max = size - 2

    i = 0
    dirs_i = 0
    value = 1
    while value <= size ** 2:
        print(f'x: {x}, y: {y}, value: {value}, left_max: {left_max}, right_max: {right_max}, top_max: {top_max}, bottom_max: {bottom_max}')
        inner_x, inner_y = dirs[dirs_i]
        arr[size * y + x] = value
        if inner_x != 0:
            if inner_x > 0:
                if x <= right_max:
                    x += inner_x
                    if x == right_max:
                        right_max -= 1
                        dirs_i = (dirs_i + 1) % size
            else:
                if x >= left_max:
                    x += inner_x
                    if x == left_max:
                        left_max += 1
                        dirs_i = (dirs_i + 1) % size
        else:  # inner_y != 0
            if inner_y > 0:
                if y <= bottom_max:
                    y += inner_y
                    if y == bottom_max:
                        bottom_max -= 1
                        dirs_i = (dirs_i + 1) % size
            else:
                if y >= top_max:
                    y += inner_y
                    if y == top_max:
                        top_max += 1
                        dirs_i = (dirs_i + 1) % size
        value += 1
        i += 1

    print(arr, left, top, direction)

    arr[arr.index(size ** 2)] = 0
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
    size = 3
    PuzzleSolver.print(spiral(size, left=True, top=True, direction=True)[0], size)
    PuzzleSolver.print(spiral(size, left=True, top=True, direction=False)[0], size)
    PuzzleSolver.print(spiral(size, left=False, top=True, direction=True)[0], size)
    PuzzleSolver.print(spiral(size, left=False, top=True, direction=False)[0], size)
    PuzzleSolver.print(spiral(size, left=True, top=False, direction=True)[0], size)
    PuzzleSolver.print(spiral(size, left=True, top=False, direction=False)[0], size)
    PuzzleSolver.print(spiral(size, left=False, top=False, direction=True)[0], size)
    PuzzleSolver.print(spiral(size, left=False, top=False, direction=False)[0], size)


if __name__ == '__main__':
    main()
