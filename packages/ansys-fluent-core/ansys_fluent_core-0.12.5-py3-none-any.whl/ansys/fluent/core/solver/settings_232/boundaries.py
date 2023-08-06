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
from .boundaries_child import boundaries_child

class boundaries(NamedObject[boundaries_child], _CreatableNamedObjectMixin[boundaries_child]):
    """
    'boundaries' child.
    """

    fluent_name = "boundaries"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of boundaries.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of boundaries.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of boundaries.
    """
    child_object_type: boundaries_child = boundaries_child
    """
    child_object_type of boundaries.
    """
