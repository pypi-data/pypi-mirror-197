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
from .exhaust_fan_child import exhaust_fan_child

class exhaust_fan(NamedObject[exhaust_fan_child], _NonCreatableNamedObjectMixin[exhaust_fan_child]):
    """
    'exhaust_fan' child.
    """

    fluent_name = "exhaust-fan"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of exhaust_fan.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of exhaust_fan.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of exhaust_fan.
    """
    child_object_type: exhaust_fan_child = exhaust_fan_child
    """
    child_object_type of exhaust_fan.
    """
