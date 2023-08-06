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
from .axis_child import axis_child

class degassing(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    """
    'degassing' child.
    """

    fluent_name = "degassing"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of degassing.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of degassing.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of degassing.
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of degassing.
    """
