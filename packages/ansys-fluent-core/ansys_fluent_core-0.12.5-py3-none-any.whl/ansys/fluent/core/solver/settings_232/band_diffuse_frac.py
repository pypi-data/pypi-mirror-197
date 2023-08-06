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
from .axis_direction_child import axis_direction_child

class band_diffuse_frac(NamedObject[axis_direction_child], _NonCreatableNamedObjectMixin[axis_direction_child]):
    """
    'band_diffuse_frac' child.
    """

    fluent_name = "band-diffuse-frac"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of band_diffuse_frac.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of band_diffuse_frac.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of band_diffuse_frac.
    """
    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of band_diffuse_frac.
    """
