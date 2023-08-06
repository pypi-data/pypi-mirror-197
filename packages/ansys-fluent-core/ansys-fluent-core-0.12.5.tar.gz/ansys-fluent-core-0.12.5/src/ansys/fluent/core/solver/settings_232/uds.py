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
from .child_object_type_child_1 import child_object_type_child

class uds(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'uds' child.
    """

    fluent_name = "uds"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of uds.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of uds.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of uds.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of uds.
    """
