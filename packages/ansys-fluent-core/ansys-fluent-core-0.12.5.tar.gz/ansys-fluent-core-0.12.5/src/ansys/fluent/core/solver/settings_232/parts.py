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
from .parts_child import parts_child

class parts(NamedObject[parts_child], _CreatableNamedObjectMixin[parts_child]):
    """
    'parts' child.
    """

    fluent_name = "parts"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of parts.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of parts.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of parts.
    """
    child_object_type: parts_child = parts_child
    """
    child_object_type of parts.
    """
