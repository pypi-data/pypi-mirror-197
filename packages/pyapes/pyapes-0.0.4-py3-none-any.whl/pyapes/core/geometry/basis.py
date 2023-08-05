#!/usr/bin/env python3
"""Basis of geometries."""
from typing import Any

DIR = ["x", "y", "z"]
DIR_TO_NUM: dict[str, int] = {"x": 0, "y": 1, "z": 2}
"""Direction to number. e.g. `x -> 0, y -> 1, z -> 2`."""
SIDE_TO_NUM: dict[str, int] = {"l": 0, "r": 1}
"""Side to number. e.g. `l -> 0, r -> 1`."""
NUM_TO_DIR: dict[int, str] = {0: "x", 1: "y", 2: "z"}
FDIR = ["xl", "xr", "yl", "yr", "zl", "zr"]  # could be used for bc identifier?
FDIR_TO_NUM: dict[str, int] = {
    "xl": 0,
    "xr": 1,
    "yl": 2,
    "yr": 3,
    "zl": 4,
    "zr": 5,
}


class GeoTypeIdentifier(list):
    """Class that helps to identify the list of types."""

    def __contains__(self, typ: type):
        for val in self:
            if isinstance(val, typ):
                return True
        return False


class Geometry:
    """Base class of all geometries.

    Note:
        - `self.X, self.Y, self.Z` indicate base of geometries. (a cylinder will have center - radius - height instead.)
    """

    @property
    def X(self) -> float:
        raise NotImplementedError

    @property
    def Y(self) -> float:
        raise NotImplementedError

    @property
    def Z(self) -> float:
        raise NotImplementedError

    @property
    def dim(self) -> int:
        """dimension of the geometry."""
        raise NotImplementedError

    @property
    def type(self) -> str:
        raise NotImplementedError

    @property
    def size(self) -> float:
        """Geometry size."""
        raise NotImplementedError

    @property
    def lower(self) -> list[float]:
        """Lower bounds of the geometry."""
        raise NotImplementedError

    @property
    def upper(self) -> list[float]:
        """Upper bounds of the geometry."""
        raise NotImplementedError

    @property
    def config(self) -> dict[int, dict[str, list[list[float]] | str]]:
        """Configuration of the geometry."""
        raise NotImplementedError

    def __eq__(self, other: Any):
        return (self.lower == other.lower) and (self.size == other.size)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lower={self.lower}, upper={self.upper}, size={self.size:.1e})"


class GeoBounder(type):
    """
    Using the set of bounds (via `__getitem__`), initialize the object.

    For example, this allows to create a box from (0, 0) to (10, 20):

    * box[0:10, 0:20]
    * box((0, 0), (10, 20))

    Note:
        - `lower` and `upper` is the list of either ints or floats. However,
          once the class is instantiated, given bounds will be converted to
          the list of floats.

    """

    def __getitem__(self, item: tuple[slice, ...] | slice):
        if not isinstance(item, tuple | slice):
            raise IndexError("GeoBounder: bounds must be a tuple of slices")

        if isinstance(item, slice):
            item = (item,)

        lower = []
        upper = []
        for dim in item:
            assert isinstance(dim, slice)
            assert type(dim.start) is float or type(dim.start) is int
            assert type(dim.stop) is float or type(dim.stop) is int
            assert dim.step is None, "GeoBounder: step must be None"

            # Lower and upper are forced to have float datatype
            lower.append(float(dim.start))
            upper.append(float(dim.stop))

        return self(lower, upper)


def bound_edge_and_corner(
    lower: list[float], upper: list[float]
) -> tuple[list[list[float]], list[list[float]], list[str], int]:
    """Crate edge and  corner information based on input dimension.

    Note:
        - Order is always from - to + (in terms of the normal vector).
        - lower and upper contains location in the order of x - y - z.
        - Currently hard-coded. Any better ideas?

    Args:
        lower: lower bounds of the box
        upper: upper bounds of the box
        dim: box dimension
    """

    dim = len(lower)

    assert dim > 0 and dim < 4, "Dimensions must be 1, 2 and 3!"

    if dim == 1:
        # 1D edge and corner
        xp = [[lower[0]], [upper[0]]]
        ex = [[lower[0] - xp[0][0]], [upper[0] - xp[1][0]]]
        face = ["xl", "xr"]
    elif dim == 2:
        # 2D edge and corner
        xp = [
            [lower[0], lower[1]],
            [lower[0], upper[1]],
            [lower[0], lower[1]],
            [upper[0], lower[1]],
        ]
        ex = [
            [upper[0] - xp[0][0], lower[1] - xp[0][1]],
            [upper[0] - xp[1][0], upper[1] - xp[1][1]],
            [lower[0] - xp[2][0], upper[1] - xp[2][1]],
            [upper[0] - xp[3][0], upper[1] - xp[3][1]],
        ]
        face = ["yl", "yr", "xl", "xr"]
    else:
        # 3D edge and corner
        # Set of xp
        xp = [
            [lower[0], lower[1], lower[2]],
            [upper[0], lower[1], lower[2]],
            [lower[0], lower[1], lower[2]],
            [lower[0], upper[1], lower[2]],
            [lower[0], lower[1], lower[2]],
            [lower[0], lower[1], upper[2]],
        ]
        ex = [
            [lower[0] - xp[0][0], upper[1] - xp[0][1], upper[2] - xp[0][2]],
            [upper[0] - xp[1][0], upper[1] - xp[1][1], upper[2] - xp[1][2]],
            [upper[0] - xp[2][0], lower[1] - xp[2][1], upper[2] - xp[2][2]],
            [upper[0] - xp[3][0], upper[1] - xp[3][1], upper[2] - xp[3][2]],
            [upper[0] - xp[4][0], upper[1] - xp[4][1], lower[2] - xp[4][2]],
            [upper[0] - xp[5][0], upper[1] - xp[5][1], upper[2] - xp[5][2]],
        ]
        face = ["xl", "xr", "yl", "yr", "zl", "zr"]

    return ex, xp, face, dim
