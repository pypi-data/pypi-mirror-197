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
from .periodic_child import periodic_child

class periodic(NamedObject[periodic_child], _NonCreatableNamedObjectMixin[periodic_child]):
    """
    'periodic' child.
    """

    fluent_name = "periodic"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of periodic.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of periodic.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of periodic.
    """
    child_object_type: periodic_child = periodic_child
    """
    child_object_type of periodic.
    """
