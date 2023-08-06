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
from .axis_child import axis_child

class geometry(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'geometry' child.
    """

    fluent_name = "geometry"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of geometry.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of geometry.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of geometry.
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of geometry.
    """
