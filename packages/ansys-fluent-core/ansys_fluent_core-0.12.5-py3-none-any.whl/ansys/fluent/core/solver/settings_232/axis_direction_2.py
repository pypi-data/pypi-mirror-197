#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .axis_direction_child import axis_direction_child

class axis_direction(ListObject[axis_direction_child]):
    """
    'axis_direction' child.
    """

    fluent_name = "axis-direction"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of axis_direction.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of axis_direction.
    """
