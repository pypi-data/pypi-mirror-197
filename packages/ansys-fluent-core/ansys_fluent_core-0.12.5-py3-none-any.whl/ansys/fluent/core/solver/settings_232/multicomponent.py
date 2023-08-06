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
from .multicomponent_child import multicomponent_child

class multicomponent(NamedObject[multicomponent_child], _NonCreatableNamedObjectMixin[multicomponent_child]):
    """
    'multicomponent' child.
    """

    fluent_name = "multicomponent"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of multicomponent.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of multicomponent.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of multicomponent.
    """
    child_object_type: multicomponent_child = multicomponent_child
    """
    child_object_type of multicomponent.
    """
