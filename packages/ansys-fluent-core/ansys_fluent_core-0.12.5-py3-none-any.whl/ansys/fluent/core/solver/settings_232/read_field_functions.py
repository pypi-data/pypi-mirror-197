#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_1 import file_name
class read_field_functions(Command):
    """
    Read custom field-function definitions from a file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "read-field-functions"

    argument_names = \
        ['file_name']

    file_name: file_name = file_name
    """
    file_name argument of read_field_functions.
    """
