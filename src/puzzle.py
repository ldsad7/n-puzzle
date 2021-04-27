from typing import Optional, Tuple, NewType

# [arr, cost, prev_puzzle]
Puzzle = NewType('Puzzle', Tuple[Tuple[int], int, Optional['Puzzle']])
