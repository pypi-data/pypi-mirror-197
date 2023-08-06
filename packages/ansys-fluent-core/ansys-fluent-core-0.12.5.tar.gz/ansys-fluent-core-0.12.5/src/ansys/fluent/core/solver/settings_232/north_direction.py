#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .north_x import north_x
from .north_y import north_y
from .north_z import north_z
class north_direction(Group):
    """
    'north_direction' child.
    """

    fluent_name = "north-direction"

    child_names = \
        ['north_x', 'north_y', 'north_z']

    north_x: north_x = north_x
    """
    north_x child of north_direction.
    """
    north_y: north_y = north_y
    """
    north_y child of north_direction.
    """
    north_z: north_z = north_z
    """
    north_z child of north_direction.
    """
