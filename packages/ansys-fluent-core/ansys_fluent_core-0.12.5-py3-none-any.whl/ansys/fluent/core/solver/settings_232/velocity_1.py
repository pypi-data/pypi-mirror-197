#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .child_object_type_child_1 import child_object_type_child

class velocity(ListObject[child_object_type_child]):
    """
    'velocity' child.
    """

    fluent_name = "velocity"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of velocity.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of velocity.
    """
