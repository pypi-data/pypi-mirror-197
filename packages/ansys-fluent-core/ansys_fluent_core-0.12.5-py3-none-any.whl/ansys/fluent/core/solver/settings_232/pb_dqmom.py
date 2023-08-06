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

class pb_dqmom(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'pb_dqmom' child.
    """

    fluent_name = "pb-dqmom"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of pb_dqmom.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pb_dqmom.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pb_dqmom.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of pb_dqmom.
    """
