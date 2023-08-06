#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list import list
from .list_properties import list_properties
from .duplicate import duplicate
from .axis_direction_child import axis_direction_child

class set_damping_strengths(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'set_damping_strengths' child.
    """

    fluent_name = "set-damping-strengths"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of set_damping_strengths.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of set_damping_strengths.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of set_damping_strengths.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of set_damping_strengths.
    """
