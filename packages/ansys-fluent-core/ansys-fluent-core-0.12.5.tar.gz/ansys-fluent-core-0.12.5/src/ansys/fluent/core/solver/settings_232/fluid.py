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
from .fluid_child import fluid_child

class fluid(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'fluid' child.
    """

    fluent_name = "fluid"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of fluid.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of fluid.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of fluid.
    """
    child_object_type: fluid_child = fluid_child
    """
    child_object_type of fluid.
    """
