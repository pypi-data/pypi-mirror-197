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
from .single_val_expression_child import single_val_expression_child

class single_val_expression(NamedObject[single_val_expression_child], _CreatableNamedObjectMixin[single_val_expression_child]):
    """
    'single_val_expression' child.
    """

    fluent_name = "single-val-expression"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of single_val_expression.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of single_val_expression.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of single_val_expression.
    """
    child_object_type: single_val_expression_child = single_val_expression_child
    """
    child_object_type of single_val_expression.
    """
