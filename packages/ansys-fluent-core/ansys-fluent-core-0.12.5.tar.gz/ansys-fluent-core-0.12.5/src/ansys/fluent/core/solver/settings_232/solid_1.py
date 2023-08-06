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
from .solid_child_1 import solid_child

class solid(NamedObject[solid_child], _NonCreatableNamedObjectMixin[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of solid.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of solid.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of solid.
    """
    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
