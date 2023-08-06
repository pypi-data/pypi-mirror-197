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
from .pathline_child import pathline_child

class pathline(NamedObject[pathline_child], _CreatableNamedObjectMixin[pathline_child]):
    """
    'pathline' child.
    """

    fluent_name = "pathline"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'display', 'copy',
         'add_to_graphics', 'clear_history']

    list: list = list
    """
    list command of pathline.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of pathline.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of pathline.
    """
    display: display = display
    """
    display command of pathline.
    """
    copy: copy = copy
    """
    copy command of pathline.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of pathline.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of pathline.
    """
    child_object_type: pathline_child = pathline_child
    """
    child_object_type of pathline.
    """
