#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
from .orthotropic_structure_te import orthotropic_structure_te
from .user_defined_function import user_defined_function
class struct_thermal_expansion(Group):
    """
    'struct_thermal_expansion' child.
    """

    fluent_name = "struct-thermal-expansion"

    child_names = \
        ['option', 'value', 'orthotropic_structure_te',
         'user_defined_function']

    option: option = option
    """
    option child of struct_thermal_expansion.
    """
    value: value = value
    """
    value child of struct_thermal_expansion.
    """
    orthotropic_structure_te: orthotropic_structure_te = orthotropic_structure_te
    """
    orthotropic_structure_te child of struct_thermal_expansion.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of struct_thermal_expansion.
    """
