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
from .mass_flow_inlet_child import mass_flow_inlet_child

class mass_flow_inlet(NamedObject[mass_flow_inlet_child], _NonCreatableNamedObjectMixin[mass_flow_inlet_child]):
    """
    'mass_flow_inlet' child.
    """

    fluent_name = "mass-flow-inlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of mass_flow_inlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of mass_flow_inlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of mass_flow_inlet.
    """
    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_inlet.
    """
