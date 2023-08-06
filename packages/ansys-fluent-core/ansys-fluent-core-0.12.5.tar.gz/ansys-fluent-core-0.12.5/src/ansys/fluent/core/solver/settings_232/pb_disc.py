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
from .child_object_type_child_1 import child_object_type_child

class pb_disc(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'pb_disc' child.
    """

    fluent_name = "pb-disc"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of pb_disc.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pb_disc.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pb_disc.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_disc.
    """
