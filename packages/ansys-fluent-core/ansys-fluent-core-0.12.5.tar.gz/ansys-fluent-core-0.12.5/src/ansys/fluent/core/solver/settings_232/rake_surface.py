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
from .rake_surface_child import rake_surface_child

class rake_surface(NamedObject[rake_surface_child], _CreatableNamedObjectMixin[rake_surface_child]):
    """
    'rake_surface' child.
    """

    fluent_name = "rake-surface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of rake_surface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of rake_surface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of rake_surface.
    """
    child_object_type: rake_surface_child = rake_surface_child
    """
    child_object_type of rake_surface.
    """
