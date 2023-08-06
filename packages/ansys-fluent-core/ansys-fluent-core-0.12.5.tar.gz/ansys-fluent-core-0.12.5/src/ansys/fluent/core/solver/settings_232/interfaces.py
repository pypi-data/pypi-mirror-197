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
from .interfaces_child import interfaces_child

class interfaces(NamedObject[interfaces_child], _CreatableNamedObjectMixin[interfaces_child]):
    """
    'interfaces' child.
    """

    fluent_name = "interfaces"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of interfaces.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of interfaces.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of interfaces.
    """
    child_object_type: interfaces_child = interfaces_child
    """
    child_object_type of interfaces.
    """
