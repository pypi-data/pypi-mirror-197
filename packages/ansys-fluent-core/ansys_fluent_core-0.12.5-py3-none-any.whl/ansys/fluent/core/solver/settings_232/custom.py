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
from .phase_child_10 import phase_child

class custom(NamedObject[phase_child], _CreatableNamedObjectMixin[phase_child]):
    """
    'custom' child.
    """

    fluent_name = "custom"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of custom.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of custom.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of custom.
    """
    child_object_type: phase_child = phase_child
    """
    child_object_type of custom.
    """
