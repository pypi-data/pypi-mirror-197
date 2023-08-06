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
from .point_surface_child import point_surface_child

class point_surface(NamedObject[point_surface_child], _CreatableNamedObjectMixin[point_surface_child]):
    """
    'point_surface' child.
    """

    fluent_name = "point-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of point_surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of point_surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of point_surface.
    """
    child_object_type: point_surface_child = point_surface_child
    """
    child_object_type of point_surface.
    """
