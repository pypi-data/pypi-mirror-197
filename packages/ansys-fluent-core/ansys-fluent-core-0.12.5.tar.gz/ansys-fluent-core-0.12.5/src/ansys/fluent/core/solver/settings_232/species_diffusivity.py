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
from .species_diffusivity_child import species_diffusivity_child

class species_diffusivity(NamedObject[species_diffusivity_child], _NonCreatableNamedObjectMixin[species_diffusivity_child]):
    """
    'species_diffusivity' child.
    """

    fluent_name = "species-diffusivity"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of species_diffusivity.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of species_diffusivity.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of species_diffusivity.
    """
    child_object_type: species_diffusivity_child = species_diffusivity_child
    """
    child_object_type of species_diffusivity.
    """
