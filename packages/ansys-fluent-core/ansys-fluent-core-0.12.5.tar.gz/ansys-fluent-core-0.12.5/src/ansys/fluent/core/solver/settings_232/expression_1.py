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
from .expression_child import expression_child

class expression(NamedObject[expression_child], _CreatableNamedObjectMixin[expression_child]):
    """
    'expression' child.
    """

    fluent_name = "expression"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of expression.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of expression.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of expression.
    """
    child_object_type: expression_child = expression_child
    """
    child_object_type of expression.
    """
