#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .volumes import volumes
from .interfaces import interfaces
from .list_physics import list_physics
class physics(Group):
    """
    'physics' child.
    """

    fluent_name = "physics"

    child_names = \
        ['volumes', 'interfaces']

    volumes: volumes = volumes
    """
    volumes child of physics.
    """
    interfaces: interfaces = interfaces
    """
    interfaces child of physics.
    """
    command_names = \
        ['list_physics']

    list_physics: list_physics = list_physics
    """
    list_physics command of physics.
    """
