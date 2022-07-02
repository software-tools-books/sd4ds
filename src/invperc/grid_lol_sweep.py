import random

from .grid_base import GridBase

class GridListOfListsSweep(GridBase):
    """Invasion percolation using full sweep on list of lists."""

    def _find(self):
        """Find the next cell to fill."""
        best, vx, vy = None, None, None
        for ix in range(self.nx):
            for iy in range(self.ny):
                point = (ix, iy)
                v = self._get(point)
                if v == FILLED:
                    continue
                if not self._candidate(point):
                    continue
                if (best is None) or (v > best):
                    v, vx, vy = v, ix, iy
        return (vx, vy)


    def _candidate(self, point):
        """Is this point fillable?"""
        px, py = point
        for ix in (px - 1, px + 1):
            for iy in (py - 1, py + 1):
                temp = (ix, iy)
                if not self._in_grid(temp):
                    continue
                if self._get(temp) == self.FILLED:
                    return True
        return False


    def _get(self, point):
        """Fill in a cell."""
        px, py = point
        return self._grid[px][py]


    def _make(self):
        """Create grid."""
        self._grid = []
        for x in range(self.nx):
            self._grid.append([None] * self.ny)


    def _set(self, point, value):
        """Fill in a cell."""
        px, py = point
        self._grid[px][py] = value
