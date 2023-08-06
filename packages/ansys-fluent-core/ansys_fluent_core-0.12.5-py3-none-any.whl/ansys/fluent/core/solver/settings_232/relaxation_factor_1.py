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

class relaxation_factor(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'relaxation_factor' child.
    """

    fluent_name = "relaxation-factor"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of relaxation_factor.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of relaxation_factor.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of relaxation_factor.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of relaxation_factor.
    """
