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
from .defaults_child import defaults_child

class defaults(NamedObject[defaults_child], _NonCreatableNamedObjectMixin[defaults_child]):
    """
    'defaults' child.
    """

    fluent_name = "defaults"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of defaults.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of defaults.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of defaults.
    """
    child_object_type: defaults_child = defaults_child
    """
    child_object_type of defaults.
    """
