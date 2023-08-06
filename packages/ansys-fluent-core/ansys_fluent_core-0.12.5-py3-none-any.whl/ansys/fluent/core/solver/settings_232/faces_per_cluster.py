#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_1 import option
from .global_faces_per_surface_cluster import global_faces_per_surface_cluster
from .maximum_faces_per_surface_cluster import maximum_faces_per_surface_cluster
class faces_per_cluster(Group):
    """
    'faces_per_cluster' child.
    """

    fluent_name = "faces-per-cluster"

    child_names = \
        ['option', 'global_faces_per_surface_cluster',
         'maximum_faces_per_surface_cluster']

    option: option = option
    """
    option child of faces_per_cluster.
    """
    global_faces_per_surface_cluster: global_faces_per_surface_cluster = global_faces_per_surface_cluster
    """
    global_faces_per_surface_cluster child of faces_per_cluster.
    """
    maximum_faces_per_surface_cluster: maximum_faces_per_surface_cluster = maximum_faces_per_surface_cluster
    """
    maximum_faces_per_surface_cluster child of faces_per_cluster.
    """
