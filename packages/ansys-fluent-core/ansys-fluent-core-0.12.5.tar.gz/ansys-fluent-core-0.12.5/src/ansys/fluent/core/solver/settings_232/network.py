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
from .network_child import network_child

class network(NamedObject[network_child], _NonCreatableNamedObjectMixin[network_child]):
    """
    'network' child.
    """

    fluent_name = "network"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of network.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of network.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of network.
    """
    child_object_type: network_child = network_child
    """
    child_object_type of network.
    """
