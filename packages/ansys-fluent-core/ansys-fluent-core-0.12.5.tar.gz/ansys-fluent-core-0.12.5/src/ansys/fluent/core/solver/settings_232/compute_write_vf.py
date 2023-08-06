#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_1 import file_name
class compute_write_vf(Command):
    """
    Compute/write surface clusters and view factors for S2S radiation model.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "compute-write-vf"

    argument_names = \
        ['file_name']

    file_name: file_name = file_name
    """
    file_name argument of compute_write_vf.
    """
