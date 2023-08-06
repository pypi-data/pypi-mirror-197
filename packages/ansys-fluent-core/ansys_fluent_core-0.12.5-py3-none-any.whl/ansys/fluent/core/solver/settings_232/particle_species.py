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
from .droplet_particle_child import droplet_particle_child

class particle_species(NamedObject[droplet_particle_child], _CreatableNamedObjectMixin[droplet_particle_child]):
    """
    'particle_species' child.
    """

    fluent_name = "particle-species"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of particle_species.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of particle_species.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of particle_species.
    """
    child_object_type: droplet_particle_child = droplet_particle_child
    """
    child_object_type of particle_species.
    """
