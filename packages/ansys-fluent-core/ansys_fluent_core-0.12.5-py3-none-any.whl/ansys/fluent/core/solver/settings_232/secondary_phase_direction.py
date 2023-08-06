#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .child_object_type_child_1 import child_object_type_child

class secondary_phase_direction(ListObject[child_object_type_child]):
    """
    'secondary_phase_direction' child.
    """

    fluent_name = "secondary-phase-direction"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of secondary_phase_direction.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of secondary_phase_direction.
    """
