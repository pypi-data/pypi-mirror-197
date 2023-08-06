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
from .uds_diffusivities_child import uds_diffusivities_child

class uds_diffusivities(NamedObject[uds_diffusivities_child], _NonCreatableNamedObjectMixin[uds_diffusivities_child]):
    """
    'uds_diffusivities' child.
    """

    fluent_name = "uds-diffusivities"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of uds_diffusivities.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of uds_diffusivities.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of uds_diffusivities.
    """
    child_object_type: uds_diffusivities_child = uds_diffusivities_child
    """
    child_object_type of uds_diffusivities.
    """
