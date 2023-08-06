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
from .rans_les_interface_child import rans_les_interface_child

class rans_les_interface(NamedObject[rans_les_interface_child], _NonCreatableNamedObjectMixin[rans_les_interface_child]):
    """
    'rans_les_interface' child.
    """

    fluent_name = "rans-les-interface"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of rans_les_interface.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of rans_les_interface.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of rans_les_interface.
    """
    child_object_type: rans_les_interface_child = rans_les_interface_child
    """
    child_object_type of rans_les_interface.
    """
