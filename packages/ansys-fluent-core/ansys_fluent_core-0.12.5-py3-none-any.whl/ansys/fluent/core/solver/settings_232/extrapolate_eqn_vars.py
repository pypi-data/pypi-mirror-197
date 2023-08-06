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
from .multi_component_diffusion_mf_child import multi_component_diffusion_mf_child

class extrapolate_eqn_vars(NamedObject[multi_component_diffusion_mf_child], _NonCreatableNamedObjectMixin[multi_component_diffusion_mf_child]):
    """
    Enter the extrapolation menu.
    """

    fluent_name = "extrapolate-eqn-vars"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of extrapolate_eqn_vars.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of extrapolate_eqn_vars.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of extrapolate_eqn_vars.
    """
    child_object_type: multi_component_diffusion_mf_child = multi_component_diffusion_mf_child
    """
    child_object_type of extrapolate_eqn_vars.
    """
