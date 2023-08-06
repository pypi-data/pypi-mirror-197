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
from .plane_surface_child import plane_surface_child

class plane_surface(NamedObject[plane_surface_child], _CreatableNamedObjectMixin[plane_surface_child]):
    """
    'plane_surface' child.
    """

    fluent_name = "plane-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of plane_surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of plane_surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of plane_surface.
    """
    child_object_type: plane_surface_child = plane_surface_child
    """
    child_object_type of plane_surface.
    """
