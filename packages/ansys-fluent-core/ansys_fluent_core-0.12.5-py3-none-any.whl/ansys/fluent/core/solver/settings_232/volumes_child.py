#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_2 import type
from .boundaries import boundaries
from .locations import locations
class volumes_child(Group):
    """
    'child_object_type' of volumes.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'boundaries', 'locations']

    type: type = type
    """
    type child of volumes_child.
    """
    boundaries: boundaries = boundaries
    """
    boundaries child of volumes_child.
    """
    locations: locations = locations
    """
    locations child of volumes_child.
    """
