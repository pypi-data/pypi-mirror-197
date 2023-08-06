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
from .display_1 import display
from .copy_3 import copy
from .add_to_graphics import add_to_graphics
from .clear_history import clear_history
from .olic_child import olic_child

class olic(NamedObject[olic_child], _CreatableNamedObjectMixin[olic_child]):
    """
    'olic' child.
    """

    fluent_name = "olic"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'display', 'copy',
         'add_to_graphics', 'clear_history']

    list: list = list
    """
    list command of olic.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of olic.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of olic.
    """
    display: display = display
    """
    display command of olic.
    """
    copy: copy = copy
    """
    copy command of olic.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of olic.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of olic.
    """
    child_object_type: olic_child = olic_child
    """
    child_object_type of olic.
    """
