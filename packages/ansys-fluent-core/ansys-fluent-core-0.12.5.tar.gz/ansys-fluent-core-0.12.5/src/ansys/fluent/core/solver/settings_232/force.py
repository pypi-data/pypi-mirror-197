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

class force(NamedObject[force_child], _CreatableNamedObjectMixin[force_child]):
    """
    'force' child.
    """

    fluent_name = "force"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of force.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of force.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of force.
    """
    child_object_type: force_child = force_child
    """
    child_object_type of force.
    """
