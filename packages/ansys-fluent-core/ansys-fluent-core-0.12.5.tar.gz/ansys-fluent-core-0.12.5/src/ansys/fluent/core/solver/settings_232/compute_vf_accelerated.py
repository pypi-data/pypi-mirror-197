#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_1 import file_name
class compute_vf_accelerated(Command):
    """
    Compute/Write view factors from existing surface clusters.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "compute-vf-accelerated"

    argument_names = \
        ['file_name']

    file_name: file_name = file_name
    """
    file_name argument of compute_vf_accelerated.
    """
