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

class adhesion_angle(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'adhesion_angle' child.
    """

    fluent_name = "adhesion-angle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of adhesion_angle.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of adhesion_angle.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of adhesion_angle.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of adhesion_angle.
    """
