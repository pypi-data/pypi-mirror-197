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
from .phase_child import phase_child

class phase(NamedObject[phase_child], _NonCreatableNamedObjectMixin[phase_child]):
    """
    'phase' child.
    """

    fluent_name = "phase"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of phase.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of phase.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of phase.
    """
    child_object_type: phase_child = phase_child
    """
    child_object_type of phase.
    """
