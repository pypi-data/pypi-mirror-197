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
from .inlet_vent_child import inlet_vent_child

class inlet_vent(NamedObject[inlet_vent_child], _NonCreatableNamedObjectMixin[inlet_vent_child]):
    """
    'inlet_vent' child.
    """

    fluent_name = "inlet-vent"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of inlet_vent.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of inlet_vent.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of inlet_vent.
    """
    child_object_type: inlet_vent_child = inlet_vent_child
    """
    child_object_type of inlet_vent.
    """
