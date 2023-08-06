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
from .set_velocity_and_vof_cutoffs_child import set_velocity_and_vof_cutoffs_child

class set_velocity_and_vof_cutoffs(NamedObject[set_velocity_and_vof_cutoffs_child], _NonCreatableNamedObjectMixin[set_velocity_and_vof_cutoffs_child]):
    """
    'set_velocity_and_vof_cutoffs' child.
    """

    fluent_name = "set-velocity-and-vof-cutoffs"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of set_velocity_and_vof_cutoffs.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of set_velocity_and_vof_cutoffs.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of set_velocity_and_vof_cutoffs.
    """
    child_object_type: set_velocity_and_vof_cutoffs_child = set_velocity_and_vof_cutoffs_child
    """
    child_object_type of set_velocity_and_vof_cutoffs.
    """
