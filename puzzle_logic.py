import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Puzzle:
    """Manage puzzle state and movement logic."""

    grid_size: int = 4

    def __post_init__(self):
        self.tile_count = self.grid_size ** 2
        self.reset()

    def reset(self) -> None:
        """Initialize puzzle in solved state."""
        self.tiles: List[int] = list(range(self.tile_count))
        # ``blank`` stores the **index position** of the empty tile
        self.blank = self.tile_count - 1
        self.moves = 0

    # helpers
    def index(self, row: int, col: int) -> int:
        return row * self.grid_size + col

    def coords(self, index: int) -> Tuple[int, int]:
        return divmod(index, self.grid_size)

    def is_adjacent(self, idx: int) -> bool:
        r, c = self.coords(idx)
        br, bc = self.coords(self.blank)
        return (abs(r - br) == 1 and c == bc) or (abs(c - bc) == 1 and r == br)

    def move_tile(self, idx: int) -> bool:
        """Attempt to move the tile at ``idx``. Return True if moved."""
        if not self.is_adjacent(idx):
            return False
        self.tiles[self.blank], self.tiles[idx] = self.tiles[idx], self.tiles[self.blank]
        self.blank = idx
        self.moves += 1
        return True

    def move_blank(self, dr: int, dc: int) -> bool:
        """Move blank tile by (dr, dc) if possible."""
        br, bc = self.coords(self.blank)
        nr, nc = br + dr, bc + dc
        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
            idx = self.index(nr, nc)
            return self.move_tile(idx)
        return False

    def shuffled(self) -> None:
        """Shuffle tiles into a random, solvable state."""
        arr = list(range(self.tile_count))
        while True:
            random.shuffle(arr)
            if self.is_solvable(arr) and arr != list(range(self.tile_count)):
                break
        self.tiles = arr
        self.blank = arr.index(self.tile_count - 1)
        self.moves = 0

    def inversions(self, arr: List[int]) -> int:
        inv = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] != self.tile_count - 1 and arr[j] != self.tile_count - 1 and arr[i] > arr[j]:
                    inv += 1
        return inv

    def is_solvable(self, arr: List[int]) -> bool:
        inv = self.inversions(arr)
        blank_row = self.grid_size - (arr.index(self.tile_count - 1) // self.grid_size)
        if self.grid_size % 2 == 1:
            return inv % 2 == 0
        return (inv + blank_row) % 2 == 0

    def is_solved(self) -> bool:
        return self.tiles == list(range(self.tile_count))
