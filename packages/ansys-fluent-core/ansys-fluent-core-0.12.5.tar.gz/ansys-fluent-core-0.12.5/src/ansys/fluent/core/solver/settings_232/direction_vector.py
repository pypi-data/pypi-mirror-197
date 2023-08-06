#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .child_object_type_child_1 import child_object_type_child

class direction_vector(ListObject[child_object_type_child]):
    """
    'direction_vector' child.
    """

    fluent_name = "direction-vector"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of direction_vector.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of direction_vector.
    """
