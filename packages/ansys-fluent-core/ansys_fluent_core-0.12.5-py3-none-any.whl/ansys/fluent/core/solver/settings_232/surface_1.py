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
from .surface_child import surface_child

class surface(NamedObject[surface_child], _CreatableNamedObjectMixin[surface_child]):
    """
    'surface' child.
    """

    fluent_name = "surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of surface.
    """
    child_object_type: surface_child = surface_child
    """
    child_object_type of surface.
    """
