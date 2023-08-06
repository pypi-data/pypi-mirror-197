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
from .wall_child import wall_child

class wall(NamedObject[wall_child], _NonCreatableNamedObjectMixin[wall_child]):
    """
    'wall' child.
    """

    fluent_name = "wall"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of wall.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of wall.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of wall.
    """
    child_object_type: wall_child = wall_child
    """
    child_object_type of wall.
    """
