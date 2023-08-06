#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_1 import file_name
class read_profile(Command):
    """
    Read boundary profile data (*.prof, *.csv). Default is *.prof.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "read-profile"

    argument_names = \
        ['file_name']

    file_name: file_name = file_name
    """
    file_name argument of read_profile.
    """
