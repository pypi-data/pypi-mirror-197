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
from .radiator_child import radiator_child

class radiator(NamedObject[radiator_child], _NonCreatableNamedObjectMixin[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of radiator.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of radiator.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of radiator.
    """
    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
