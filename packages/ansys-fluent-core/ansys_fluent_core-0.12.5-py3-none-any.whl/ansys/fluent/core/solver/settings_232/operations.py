#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .coarsen import coarsen
from .refine import refine
from .swap import swap
from .move import move
class operations(Group):
    """
    Enter the anisotropic adaption operations menu.
    """

    fluent_name = "operations"

    child_names = \
        ['coarsen', 'refine', 'swap', 'move']

    coarsen: coarsen = coarsen
    """
    coarsen child of operations.
    """
    refine: refine = refine
    """
    refine child of operations.
    """
    swap: swap = swap
    """
    swap child of operations.
    """
    move: move = move
    """
    move child of operations.
    """
