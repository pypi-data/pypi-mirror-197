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
from .intake_fan_child import intake_fan_child

class intake_fan(NamedObject[intake_fan_child], _NonCreatableNamedObjectMixin[intake_fan_child]):
    """
    'intake_fan' child.
    """

    fluent_name = "intake-fan"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of intake_fan.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of intake_fan.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of intake_fan.
    """
    child_object_type: intake_fan_child = intake_fan_child
    """
    child_object_type of intake_fan.
    """
