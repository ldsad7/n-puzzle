from typing import Optional, Tuple, NewType

# [arr, cost, prev_puzzle]
Puzzle = NewType('Puzzle', Tuple[Tuple[int, ...], float, Optional['Puzzle']])
