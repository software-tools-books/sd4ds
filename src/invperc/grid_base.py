from abc import ABC

class GridBase(ABC):
    """Invasion percolation."""

    # Marker for filled cells.
    FILLED = -1.0

    def __init__(self, nx, ny):
        """Common initialization."""
        assert nx > 0 and ny > 0
        self.nx = nx
        self.ny = ny
        self._initialize()


    def evolve(self):
        """Keep filling until done."""
        latest = (self.nx // 2, self.ny // 2)
        self._set(latest, self.FILLED)
        while not self._finished(latest):
            latest = self._find()
            self._fill(latest)


    def _in_grid(self, point):
        """Is this point in the grid?"""
        x, y = point
        return (0 <= x) and (x < self.nx) and (0 <= y) and (y < self.ny)


    def _initialize(self):
        """Create and fill the grid."""
        self._make()
        for ix in range(self.nx):
            for iy in range(self.ny):
                self._set((ix, iy), random.random())


    def __str__(self):
        """Printable representation."""
        result = ""
        for iy in range(self.ny - 1, -1, -1):
            for ix in range(self.nx):
                result += "*" if (self._get((ix, iy)) == self.FILLED) else " "
            result += "\n"
        return result


    @abstractmethod
    def _find(self):
        """Find the next cell to fill."""


    @abstractmethod
    def _get(self, point):
        """Get the value of a cell."""


    @abstractmethod
    def _make(self):
        """Create grid."""


    @abstractmethod
    def _set(self, point, value):
        """Fill in a cell."""
