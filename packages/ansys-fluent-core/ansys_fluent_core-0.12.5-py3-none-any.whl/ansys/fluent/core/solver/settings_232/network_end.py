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
from .network_end_child import network_end_child

class network_end(NamedObject[network_end_child], _NonCreatableNamedObjectMixin[network_end_child]):
    """
    'network_end' child.
    """

    fluent_name = "network-end"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of network_end.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of network_end.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of network_end.
    """
    child_object_type: network_end_child = network_end_child
    """
    child_object_type of network_end.
    """
