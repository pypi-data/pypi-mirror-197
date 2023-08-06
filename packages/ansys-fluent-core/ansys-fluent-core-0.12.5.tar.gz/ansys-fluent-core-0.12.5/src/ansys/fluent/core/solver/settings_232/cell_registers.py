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
from .cell_registers_child import cell_registers_child

class cell_registers(NamedObject[cell_registers_child], _CreatableNamedObjectMixin[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of cell_registers.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of cell_registers.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of cell_registers.
    """
    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
