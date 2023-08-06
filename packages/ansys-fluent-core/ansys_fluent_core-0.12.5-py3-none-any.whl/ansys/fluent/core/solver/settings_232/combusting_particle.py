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
from .combusting_particle_child import combusting_particle_child

class combusting_particle(NamedObject[combusting_particle_child], _CreatableNamedObjectMixin[combusting_particle_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of combusting_particle.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of combusting_particle.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of combusting_particle.
    """
    child_object_type: combusting_particle_child = combusting_particle_child
    """
    child_object_type of combusting_particle.
    """
