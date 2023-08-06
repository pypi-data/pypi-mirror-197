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
from .force_child import force_child

class lift(NamedObject[force_child], _CreatableNamedObjectMixin[force_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of lift.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of lift.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of lift.
    """
    child_object_type: force_child = force_child
    """
    child_object_type of lift.
    """
