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

class global_dt_pseudo_relax(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'global_dt_pseudo_relax' child.
    """

    fluent_name = "global-dt-pseudo-relax"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of global_dt_pseudo_relax.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of global_dt_pseudo_relax.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of global_dt_pseudo_relax.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of global_dt_pseudo_relax.
    """
