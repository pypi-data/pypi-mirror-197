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
from .user_defined_child import user_defined_child

class user_defined(NamedObject[user_defined_child], _CreatableNamedObjectMixin[user_defined_child]):
    """
    'user_defined' child.
    """

    fluent_name = "user-defined"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of user_defined.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of user_defined.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of user_defined.
    """
    child_object_type: user_defined_child = user_defined_child
    """
    child_object_type of user_defined.
    """
