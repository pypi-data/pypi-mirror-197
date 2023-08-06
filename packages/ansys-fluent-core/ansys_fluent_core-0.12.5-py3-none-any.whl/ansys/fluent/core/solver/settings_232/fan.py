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
from .fan_child import fan_child

class fan(NamedObject[fan_child], _NonCreatableNamedObjectMixin[fan_child]):
    """
    'fan' child.
    """

    fluent_name = "fan"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of fan.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of fan.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of fan.
    """
    child_object_type: fan_child = fan_child
    """
    child_object_type of fan.
    """
