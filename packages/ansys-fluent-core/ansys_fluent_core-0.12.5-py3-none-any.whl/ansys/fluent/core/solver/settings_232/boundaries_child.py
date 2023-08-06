#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_3 import type
from .locations import locations
class boundaries_child(Group):
    """
    'child_object_type' of boundaries.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'locations']

    type: type = type
    """
    type child of boundaries_child.
    """
    locations: locations = locations
    """
    locations child of boundaries_child.
    """
