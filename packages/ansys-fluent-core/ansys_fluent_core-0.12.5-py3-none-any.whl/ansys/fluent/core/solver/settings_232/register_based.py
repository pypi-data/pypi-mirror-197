#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_1 import list
from .list_properties_5 import list_properties
from .duplicate import duplicate
from .set_1 import set
from .register_based_child import register_based_child

class register_based(NamedObject[register_based_child], _CreatableNamedObjectMixin[register_based_child]):
    """
    Set up the application of poor mesh numerics to cells in a register.
    """

    fluent_name = "register-based"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'set']

    list: list = list
    """
    list command of register_based.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of register_based.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of register_based.
    """
    set: set = set
    """
    set command of register_based.
    """
    child_object_type: register_based_child = register_based_child
    """
    child_object_type of register_based.
    """
