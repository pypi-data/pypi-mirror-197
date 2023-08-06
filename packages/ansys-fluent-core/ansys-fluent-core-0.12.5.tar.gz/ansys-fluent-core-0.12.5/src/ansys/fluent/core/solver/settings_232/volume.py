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
from .volume_child import volume_child

class volume(NamedObject[volume_child], _CreatableNamedObjectMixin[volume_child]):
    """
    'volume' child.
    """

    fluent_name = "volume"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of volume.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of volume.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of volume.
    """
    child_object_type: volume_child = volume_child
    """
    child_object_type of volume.
    """
