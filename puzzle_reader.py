from typing import List, Optional, Tuple

from npuzzle_gen import make_puzzle
from puzzle import Puzzle


class PuzzleReader:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def read(self, path: Optional[str], size: Optional[int]) -> Puzzle:
        arr: List[int] = []
        if path is not None:
            arr, size = self._read_puzzle_from_file(path)
        elif size is not None:
            arr = self._gen_puzzle(size)
        else:
            raise ValueError(f"Incorrect arguments path='{path or ''}', size={size or 0}")
        try:
            self._validate_puzzle(arr, size)
        except AssertionError:
            raise ValueError(f"File '{path}' doesn't contain correct values from 0 to {size * size - 1}")
        return Puzzle(arr=arr, size=size, prev_puzzle=None, cost=0)

    @staticmethod
    def _validate_puzzle(arr: List[int], size: int):
        assert set(arr) == set(range(size * size))

    @staticmethod
    def _read_puzzle_from_file(path: str) -> Tuple[List[int], int]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        except Exception as ex:
            raise ValueError(f"We weren't able to open file '{path}' ({ex})")
        lines = [line for line in lines if not line.startswith('#') and line.strip()]
        if not lines:
            raise ValueError(f"File '{path}' doesn't contain any data")
        try:
            size: int = int(lines[0].strip())
        except ValueError as ex:
            raise ValueError(f"We weren't able to read size from file '{path}' ({ex})")
        assert size >= 2, f"size (given {size}) cannot be less than 2"
        assert size == len(lines) - 1, f"file '{path}' contains incorrect number of lines"
        arr: List[int] = []
        for i, line in enumerate(lines[1:], start=1):
            values = line.split()
            assert len(values) == size, f"line {i} of the file '{path}' doesn't contain {size} values"
            try:
                values = list(map(int, values))
            except ValueError as ex:
                raise ValueError(f"line {i} of the file '{path}' doesn't contain correct values ({ex})")
            arr.extend(values)
        return arr, size

    @staticmethod
    def _gen_puzzle(size: int) -> List[int]:
        return make_puzzle(size, solvable=True, iterations=10000)
