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
from .turb_visc_func_mf_child import turb_visc_func_mf_child

class uds_bc(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'uds_bc' child.
    """

    fluent_name = "uds-bc"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of uds_bc.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of uds_bc.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of uds_bc.
    """
    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of uds_bc.
    """
