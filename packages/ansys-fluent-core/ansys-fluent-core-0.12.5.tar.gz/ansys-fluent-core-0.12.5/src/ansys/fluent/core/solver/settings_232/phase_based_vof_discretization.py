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

class phase_based_vof_discretization(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'phase_based_vof_discretization' child.
    """

    fluent_name = "phase-based-vof-discretization"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of phase_based_vof_discretization.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of phase_based_vof_discretization.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of phase_based_vof_discretization.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of phase_based_vof_discretization.
    """
