#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class volatile_fraction(Group):
    """
    'volatile_fraction' child.
    """

    fluent_name = "volatile-fraction"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of volatile_fraction.
    """
    value: value = value
    """
    value child of volatile_fraction.
    """
