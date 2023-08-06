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
from .child_object_type_child import child_object_type_child

class cross_section_multicomponent_child(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'child_object_type' of cross_section_multicomponent.
    """

    fluent_name = "child-object-type"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of cross_section_multicomponent_child.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of cross_section_multicomponent_child.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of cross_section_multicomponent_child.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of cross_section_multicomponent_child.
    """
