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
from .pressure_far_field_child import pressure_far_field_child

class pressure_far_field(NamedObject[pressure_far_field_child], _NonCreatableNamedObjectMixin[pressure_far_field_child]):
    """
    'pressure_far_field' child.
    """

    fluent_name = "pressure-far-field"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of pressure_far_field.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pressure_far_field.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pressure_far_field.
    """
    child_object_type: pressure_far_field_child = pressure_far_field_child
    """
    child_object_type of pressure_far_field.
    """
