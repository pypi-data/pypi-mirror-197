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
from .groups_child import groups_child

class groups(NamedObject[groups_child], _CreatableNamedObjectMixin[groups_child]):
    """
    'groups' child.
    """

    fluent_name = "groups"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of groups.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of groups.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of groups.
    """
    child_object_type: groups_child = groups_child
    """
    child_object_type of groups.
    """
