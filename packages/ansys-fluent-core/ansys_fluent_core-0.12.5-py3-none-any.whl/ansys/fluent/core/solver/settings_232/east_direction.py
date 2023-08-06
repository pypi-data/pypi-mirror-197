#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .east_x import east_x
from .east_y import east_y
from .east_z import east_z
class east_direction(Group):
    """
    'east_direction' child.
    """

    fluent_name = "east-direction"

    child_names = \
        ['east_x', 'east_y', 'east_z']

    east_x: east_x = east_x
    """
    east_x child of east_direction.
    """
    east_y: east_y = east_y
    """
    east_y child of east_direction.
    """
    east_z: east_z = east_z
    """
    east_z child of east_direction.
    """
