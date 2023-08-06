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

class volumetric_species(NamedObject[fluid_child], _CreatableNamedObjectMixin[fluid_child]):
    """
    'volumetric_species' child.
    """

    fluent_name = "volumetric-species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of volumetric_species.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of volumetric_species.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of volumetric_species.
    """
    child_object_type: fluid_child = fluid_child
    """
    child_object_type of volumetric_species.
    """
