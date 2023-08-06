#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class averaging_coefficient_t(Group):
    """
    'averaging_coefficient_t' child.
    """

    fluent_name = "averaging-coefficient-t"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of averaging_coefficient_t.
    """
    value: value = value
    """
    value child of averaging_coefficient_t.
    """
