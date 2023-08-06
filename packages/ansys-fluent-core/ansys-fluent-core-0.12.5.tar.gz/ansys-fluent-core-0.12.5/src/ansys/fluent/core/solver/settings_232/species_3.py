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
from .species_child import species_child

class species(NamedObject[species_child], _NonCreatableNamedObjectMixin[species_child]):
    """
    'species' child.
    """

    fluent_name = "species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of species.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of species.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of species.
    """
    child_object_type: species_child = species_child
    """
    child_object_type of species.
    """
