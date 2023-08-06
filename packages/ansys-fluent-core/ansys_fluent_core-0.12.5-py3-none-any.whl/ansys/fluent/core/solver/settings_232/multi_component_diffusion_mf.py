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

class multi_component_diffusion_mf(NamedObject[multi_component_diffusion_mf_child], _NonCreatableNamedObjectMixin[multi_component_diffusion_mf_child]):
    """
    'multi_component_diffusion_mf' child.
    """

    fluent_name = "multi-component-diffusion-mf"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of multi_component_diffusion_mf.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of multi_component_diffusion_mf.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of multi_component_diffusion_mf.
    """
    child_object_type: multi_component_diffusion_mf_child = multi_component_diffusion_mf_child
    """
    child_object_type of multi_component_diffusion_mf.
    """
