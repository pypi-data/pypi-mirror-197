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
from .cross_section_multicomponent_child import cross_section_multicomponent_child

class cross_section_multicomponent(NamedObject[cross_section_multicomponent_child], _NonCreatableNamedObjectMixin[cross_section_multicomponent_child]):
    """
    'cross_section_multicomponent' child.
    """

    fluent_name = "cross-section-multicomponent"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of cross_section_multicomponent.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of cross_section_multicomponent.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of cross_section_multicomponent.
    """
    child_object_type: cross_section_multicomponent_child = cross_section_multicomponent_child
    """
    child_object_type of cross_section_multicomponent.
    """
