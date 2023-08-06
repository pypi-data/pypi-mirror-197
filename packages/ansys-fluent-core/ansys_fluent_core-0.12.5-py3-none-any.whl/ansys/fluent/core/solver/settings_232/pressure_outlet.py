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
from .pressure_outlet_child import pressure_outlet_child

class pressure_outlet(NamedObject[pressure_outlet_child], _NonCreatableNamedObjectMixin[pressure_outlet_child]):
    """
    'pressure_outlet' child.
    """

    fluent_name = "pressure-outlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of pressure_outlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pressure_outlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pressure_outlet.
    """
    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
