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
from .aeromechanics_child import aeromechanics_child

class aeromechanics(NamedObject[aeromechanics_child], _CreatableNamedObjectMixin[aeromechanics_child]):
    """
    'aeromechanics' child.
    """

    fluent_name = "aeromechanics"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of aeromechanics.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of aeromechanics.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of aeromechanics.
    """
    child_object_type: aeromechanics_child = aeromechanics_child
    """
    child_object_type of aeromechanics.
    """
