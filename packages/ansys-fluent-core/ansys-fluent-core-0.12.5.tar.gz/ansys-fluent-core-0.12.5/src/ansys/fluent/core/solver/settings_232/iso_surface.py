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
from .iso_surface_child import iso_surface_child

class iso_surface(NamedObject[iso_surface_child], _CreatableNamedObjectMixin[iso_surface_child]):
    """
    'iso_surface' child.
    """

    fluent_name = "iso-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of iso_surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of iso_surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of iso_surface.
    """
    child_object_type: iso_surface_child = iso_surface_child
    """
    child_object_type of iso_surface.
    """
