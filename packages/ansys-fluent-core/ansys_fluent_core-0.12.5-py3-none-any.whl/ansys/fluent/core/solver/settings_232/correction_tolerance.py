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
from .correction_tolerance_child import correction_tolerance_child

class correction_tolerance(NamedObject[correction_tolerance_child], _NonCreatableNamedObjectMixin[correction_tolerance_child]):
    """
    'correction_tolerance' child.
    """

    fluent_name = "correction-tolerance"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of correction_tolerance.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of correction_tolerance.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of correction_tolerance.
    """
    child_object_type: correction_tolerance_child = correction_tolerance_child
    """
    child_object_type of correction_tolerance.
    """
