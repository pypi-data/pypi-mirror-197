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
from .outflow_child import outflow_child

class outflow(NamedObject[outflow_child], _NonCreatableNamedObjectMixin[outflow_child]):
    """
    'outflow' child.
    """

    fluent_name = "outflow"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of outflow.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of outflow.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of outflow.
    """
    child_object_type: outflow_child = outflow_child
    """
    child_object_type of outflow.
    """
