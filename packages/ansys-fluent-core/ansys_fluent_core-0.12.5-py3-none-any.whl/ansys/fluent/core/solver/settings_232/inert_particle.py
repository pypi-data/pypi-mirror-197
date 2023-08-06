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
from .inert_particle_child import inert_particle_child

class inert_particle(NamedObject[inert_particle_child], _CreatableNamedObjectMixin[inert_particle_child]):
    """
    'inert_particle' child.
    """

    fluent_name = "inert-particle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of inert_particle.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of inert_particle.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of inert_particle.
    """
    child_object_type: inert_particle_child = inert_particle_child
    """
    child_object_type of inert_particle.
    """
