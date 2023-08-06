#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_1 import list_properties
from .lines_child import lines_child

class lines(ListObject[lines_child]):
    """
    'lines' child.
    """

    fluent_name = "lines"

    command_names = \
        ['list_properties']

    list_properties: list_properties = list_properties
    """
    list_properties command of lines.
    """
    child_object_type: lines_child = lines_child
    """
    child_object_type of lines.
    """
