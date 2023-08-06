#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .macro_filename import macro_filename
class execute_macro(Command):
    """
    Run a previously defined macro.
    
    Parameters
    ----------
        macro_filename : str
            'macro_filename' child.
    
    """

    fluent_name = "execute-macro"

    argument_names = \
        ['macro_filename']

    macro_filename: macro_filename = macro_filename
    """
    macro_filename argument of execute_macro.
    """
