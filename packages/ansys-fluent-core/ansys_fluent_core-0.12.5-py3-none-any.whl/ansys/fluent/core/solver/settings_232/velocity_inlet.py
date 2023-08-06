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
from .velocity_inlet_child import velocity_inlet_child

class velocity_inlet(NamedObject[velocity_inlet_child], _NonCreatableNamedObjectMixin[velocity_inlet_child]):
    """
    'velocity_inlet' child.
    """

    fluent_name = "velocity-inlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of velocity_inlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of velocity_inlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of velocity_inlet.
    """
    child_object_type: velocity_inlet_child = velocity_inlet_child
    """
    child_object_type of velocity_inlet.
    """
