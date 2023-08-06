#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .impedance_2_child import impedance_2_child

class impedance_2(ListObject[impedance_2_child]):
    """
    'impedance_2' child.
    """

    fluent_name = "impedance-2"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of impedance_2.
    """
    child_object_type: impedance_2_child = impedance_2_child
    """
    child_object_type of impedance_2.
    """
