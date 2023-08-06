#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .relaxation_factor import relaxation_factor
from .select_variables import select_variables
from .type_5 import type
class options(Group):
    """
    High Order Term Relaxation Options.
    """

    fluent_name = "options"

    child_names = \
        ['relaxation_factor', 'select_variables', 'type']

    relaxation_factor: relaxation_factor = relaxation_factor
    """
    relaxation_factor child of options.
    """
    select_variables: select_variables = select_variables
    """
    select_variables child of options.
    """
    type: type = type
    """
    type child of options.
    """
