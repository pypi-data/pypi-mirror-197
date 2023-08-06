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

class mass_flow_outlet(NamedObject[mass_flow_inlet_child], _NonCreatableNamedObjectMixin[mass_flow_inlet_child]):
    """
    'mass_flow_outlet' child.
    """

    fluent_name = "mass-flow-outlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of mass_flow_outlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of mass_flow_outlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of mass_flow_outlet.
    """
    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_outlet.
    """
