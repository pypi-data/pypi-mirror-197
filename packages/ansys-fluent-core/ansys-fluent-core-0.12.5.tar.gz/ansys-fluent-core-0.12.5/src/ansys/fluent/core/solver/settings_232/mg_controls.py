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
from .mg_controls_child import mg_controls_child

class mg_controls(NamedObject[mg_controls_child], _NonCreatableNamedObjectMixin[mg_controls_child]):
    """
    'mg_controls' child.
    """

    fluent_name = "mg-controls"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of mg_controls.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of mg_controls.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of mg_controls.
    """
    child_object_type: mg_controls_child = mg_controls_child
    """
    child_object_type of mg_controls.
    """
