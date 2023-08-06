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
from .porous_jump_child import porous_jump_child

class porous_jump(NamedObject[porous_jump_child], _NonCreatableNamedObjectMixin[porous_jump_child]):
    """
    'porous_jump' child.
    """

    fluent_name = "porous-jump"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of porous_jump.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of porous_jump.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of porous_jump.
    """
    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
