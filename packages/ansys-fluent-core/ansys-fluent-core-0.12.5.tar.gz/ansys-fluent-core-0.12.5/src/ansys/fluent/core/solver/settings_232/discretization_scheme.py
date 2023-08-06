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

class discretization_scheme(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'discretization_scheme' child.
    """

    fluent_name = "discretization-scheme"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of discretization_scheme.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of discretization_scheme.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of discretization_scheme.
    """
    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of discretization_scheme.
    """
