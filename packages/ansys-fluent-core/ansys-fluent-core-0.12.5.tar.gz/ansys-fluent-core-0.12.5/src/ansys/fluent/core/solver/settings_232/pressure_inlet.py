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
from .pressure_inlet_child import pressure_inlet_child

class pressure_inlet(NamedObject[pressure_inlet_child], _NonCreatableNamedObjectMixin[pressure_inlet_child]):
    """
    'pressure_inlet' child.
    """

    fluent_name = "pressure-inlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of pressure_inlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pressure_inlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pressure_inlet.
    """
    child_object_type: pressure_inlet_child = pressure_inlet_child
    """
    child_object_type of pressure_inlet.
    """
