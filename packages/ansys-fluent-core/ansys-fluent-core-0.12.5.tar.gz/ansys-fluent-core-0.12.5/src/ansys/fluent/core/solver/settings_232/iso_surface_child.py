#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .field import field
from .surface_2 import surface
from .zone_1 import zone
from .min import min
from .max import max
from .iso_value import iso_value
class iso_surface_child(Group):
    """
    'child_object_type' of iso_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['field', 'surface', 'zone', 'min', 'max', 'iso_value']

    field: field = field
    """
    field child of iso_surface_child.
    """
    surface: surface = surface
    """
    surface child of iso_surface_child.
    """
    zone: zone = zone
    """
    zone child of iso_surface_child.
    """
    min: min = min
    """
    min child of iso_surface_child.
    """
    max: max = max
    """
    max child of iso_surface_child.
    """
    iso_value: iso_value = iso_value
    """
    iso_value child of iso_surface_child.
    """
