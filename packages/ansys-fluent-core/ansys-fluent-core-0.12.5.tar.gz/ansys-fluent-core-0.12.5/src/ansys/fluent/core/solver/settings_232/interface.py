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
from .interface_child import interface_child

class interface(NamedObject[interface_child], _NonCreatableNamedObjectMixin[interface_child]):
    """
    'interface' child.
    """

    fluent_name = "interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of interface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of interface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of interface.
    """
    child_object_type: interface_child = interface_child
    """
    child_object_type of interface.
    """
