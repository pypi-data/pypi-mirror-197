#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class premix_heat_trans_coeff(Group):
    """
    'premix_heat_trans_coeff' child.
    """

    fluent_name = "premix-heat-trans-coeff"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of premix_heat_trans_coeff.
    """
    value: value = value
    """
    value child of premix_heat_trans_coeff.
    """
