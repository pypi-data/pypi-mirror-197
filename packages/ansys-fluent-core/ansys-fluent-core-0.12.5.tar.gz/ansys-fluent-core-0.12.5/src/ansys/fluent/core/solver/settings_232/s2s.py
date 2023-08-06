#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .viewfactor_settings import viewfactor_settings
from .clustering_settings import clustering_settings
from .radiosity_solver_control import radiosity_solver_control
from .compute_write_vf import compute_write_vf
from .compute_vf_accelerated import compute_vf_accelerated
from .compute_clusters_and_vf_accelerated import compute_clusters_and_vf_accelerated
from .compute_vf_only import compute_vf_only
from .read_vf_file import read_vf_file
class s2s(Group):
    """
    's2s' child.
    """

    fluent_name = "s2s"

    child_names = \
        ['viewfactor_settings', 'clustering_settings',
         'radiosity_solver_control']

    viewfactor_settings: viewfactor_settings = viewfactor_settings
    """
    viewfactor_settings child of s2s.
    """
    clustering_settings: clustering_settings = clustering_settings
    """
    clustering_settings child of s2s.
    """
    radiosity_solver_control: radiosity_solver_control = radiosity_solver_control
    """
    radiosity_solver_control child of s2s.
    """
    command_names = \
        ['compute_write_vf', 'compute_vf_accelerated',
         'compute_clusters_and_vf_accelerated', 'compute_vf_only',
         'read_vf_file']

    compute_write_vf: compute_write_vf = compute_write_vf
    """
    compute_write_vf command of s2s.
    """
    compute_vf_accelerated: compute_vf_accelerated = compute_vf_accelerated
    """
    compute_vf_accelerated command of s2s.
    """
    compute_clusters_and_vf_accelerated: compute_clusters_and_vf_accelerated = compute_clusters_and_vf_accelerated
    """
    compute_clusters_and_vf_accelerated command of s2s.
    """
    compute_vf_only: compute_vf_only = compute_vf_only
    """
    compute_vf_only command of s2s.
    """
    read_vf_file: read_vf_file = read_vf_file
    """
    read_vf_file command of s2s.
    """
