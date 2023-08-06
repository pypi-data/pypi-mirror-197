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
from .volumes_child import volumes_child

class volumes(NamedObject[volumes_child], _CreatableNamedObjectMixin[volumes_child]):
    """
    'volumes' child.
    """

    fluent_name = "volumes"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of volumes.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of volumes.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of volumes.
    """
    child_object_type: volumes_child = volumes_child
    """
    child_object_type of volumes.
    """
