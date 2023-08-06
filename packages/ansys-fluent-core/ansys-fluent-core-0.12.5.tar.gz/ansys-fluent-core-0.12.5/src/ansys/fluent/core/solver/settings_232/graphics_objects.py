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
from .graphics_objects_child import graphics_objects_child

class graphics_objects(NamedObject[graphics_objects_child], _CreatableNamedObjectMixin[graphics_objects_child]):
    """
    'graphics_objects' child.
    """

    fluent_name = "graphics-objects"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of graphics_objects.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of graphics_objects.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of graphics_objects.
    """
    child_object_type: graphics_objects_child = graphics_objects_child
    """
    child_object_type of graphics_objects.
    """
