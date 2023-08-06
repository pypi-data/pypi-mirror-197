#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
from .orthotropic_structure_nu import orthotropic_structure_nu
from .user_defined_function import user_defined_function
class struct_poisson_ratio(Group):
    """
    'struct_poisson_ratio' child.
    """

    fluent_name = "struct-poisson-ratio"

    child_names = \
        ['option', 'value', 'orthotropic_structure_nu',
         'user_defined_function']

    option: option = option
    """
    option child of struct_poisson_ratio.
    """
    value: value = value
    """
    value child of struct_poisson_ratio.
    """
    orthotropic_structure_nu: orthotropic_structure_nu = orthotropic_structure_nu
    """
    orthotropic_structure_nu child of struct_poisson_ratio.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of struct_poisson_ratio.
    """
