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
from .line_surface_child import line_surface_child

class line_surface(NamedObject[line_surface_child], _CreatableNamedObjectMixin[line_surface_child]):
    """
    'line_surface' child.
    """

    fluent_name = "line-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of line_surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of line_surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of line_surface.
    """
    child_object_type: line_surface_child = line_surface_child
    """
    child_object_type of line_surface.
    """
