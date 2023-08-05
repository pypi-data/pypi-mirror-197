#!/usr/bin/env python3
"""Collection of useful tools to be used in `pyABC.core.solver` module.

"""
import torch
from torch import Tensor

from pyapes.core.variables import Field


def default_A_ops(var: Field, order: int) -> list[list[Tensor]]:
    """Construct A_ops for the given order of the spatial discretization (the second order central difference scheme).

    Example:

    - Below returned results are simplified for the sake of readability.
    The actual results are the list of the tensor that has the same shape as the given `var`.

    >>> App, Ap, Ac, Am, Amm = default_A_ops(var, order=1)
    [0, ...], [1, ...], [-2, ...], [1, ...], [0, ...]
    >>> App, Ap, Ac, Am, Amm = default_A_ops(var, order=2)
    [0, ...], [1, ...], [0, ...], [-1, ...], [0, ...]

    Args:
        var (Field): The field to be discretized.
        order (int): The order of the spatial discretization. Should be either 1 or 2.

    Returns:
        list[list[Tensor]]: A_ops for the given order of the spatial discretization. The coefficients are for `i+2`, `i+1`, `i`, `i-1`, `i-2` respectively.
    """

    if order == 1:
        # Axisymmetric coordinate has same first order discretization as the cartesian case.
        App = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
        Ap = [torch.ones_like(var()) for _ in range(var.mesh.dim)]
        Ac = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
        Am = [-1.0 * torch.ones_like(var()) for _ in range(var.mesh.dim)]
        Amm = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
    elif order == 2:
        if var.mesh.coord_sys == "xyz":
            App = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
            Ap = [torch.ones_like(var()) for _ in range(var.mesh.dim)]
            Ac = [-2.0 * torch.ones_like(var()) for _ in range(var.mesh.dim)]
            Am = [torch.ones_like(var()) for _ in range(var.mesh.dim)]
            Amm = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
        else:
            r_coord = var.mesh.X
            dr = var.mesh.dx[0]

            scale = torch.nan_to_num(
                dr / (2 * r_coord), nan=0.0, posinf=0.0, neginf=0.0
            )

            App = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]
            Ap = [
                (1 + scale) * torch.ones_like(var())
                if i == 0
                else torch.ones_like(var())
                for i in range(var.mesh.dim)
            ]
            Ac = [-2.0 * torch.ones_like(var()) for _ in range(var.mesh.dim)]
            Am = [
                (1 - scale) * torch.ones_like(var())
                if i == 0
                else torch.ones_like(var())
                for i in range(var.mesh.dim)
            ]
            Amm = [torch.zeros_like(var()) for _ in range(var.mesh.dim)]

            raise NotImplementedError
    else:
        raise RuntimeError(f"Given {order=} should be either 1 or 2.")

    return [App, Ap, Ac, Am, Amm]
