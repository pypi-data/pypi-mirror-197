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
from .icing_child import icing_child

class icing(NamedObject[icing_child], _CreatableNamedObjectMixin[icing_child]):
    """
    'icing' child.
    """

    fluent_name = "icing"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of icing.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of icing.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of icing.
    """
    child_object_type: icing_child = icing_child
    """
    child_object_type of icing.
    """
