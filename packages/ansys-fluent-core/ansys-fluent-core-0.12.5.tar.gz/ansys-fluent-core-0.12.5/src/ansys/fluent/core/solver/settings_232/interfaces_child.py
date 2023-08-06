#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_4 import type
from .boundary_1 import boundary_1
from .boundary_2 import boundary_2
from .periodicity import periodicity
from .mesh_connectivity import mesh_connectivity
class interfaces_child(Group):
    """
    'child_object_type' of interfaces.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'boundary_1', 'boundary_2', 'periodicity',
         'mesh_connectivity']

    type: type = type
    """
    type child of interfaces_child.
    """
    boundary_1: boundary_1 = boundary_1
    """
    boundary_1 child of interfaces_child.
    """
    boundary_2: boundary_2 = boundary_2
    """
    boundary_2 child of interfaces_child.
    """
    periodicity: periodicity = periodicity
    """
    periodicity child of interfaces_child.
    """
    mesh_connectivity: mesh_connectivity = mesh_connectivity
    """
    mesh_connectivity child of interfaces_child.
    """
