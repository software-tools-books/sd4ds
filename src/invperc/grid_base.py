from abc import ABC
import random

class GridBase(ABC):
    """Invasion percolation."""

    # Marker for filled cells.
    FILLED = -1.0

    def __init__(self, nx, ny):
        """Common initialization."""
        assert nx > 0 and ny > 0
        self.nx = nx
        self.ny = ny
        self._make(nx, ny)


    def evolve(self):
        """Keep filling until done."""
        latest = self.initialize()
        while not self._finished(latest):
            latest = self._find()
            self._fill(latest)


    @abstractmethod
    def initialize(self):
        """Start the filling process."""
        point = (self.nx // 2, self.ny // 2)
        self._fill(point)
        return point


    @abstractmethod
    def _fill(self, point):
        """Fill in a cell."""
        pass


    @abstractmethod
    def _find(self):
        """Find the next cell to fill."""
        pass


    @abstractmethod
    def _make(self, nx, ny, filler):
        """Create grid."""
        pass
