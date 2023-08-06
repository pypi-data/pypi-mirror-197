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
from .bodies_child import bodies_child

class bodies(NamedObject[bodies_child], _CreatableNamedObjectMixin[bodies_child]):
    """
    'bodies' child.
    """

    fluent_name = "bodies"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of bodies.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of bodies.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of bodies.
    """
    child_object_type: bodies_child = bodies_child
    """
    child_object_type of bodies.
    """
