#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class melting_heat(Group):
    """
    'melting_heat' child.
    """

    fluent_name = "melting-heat"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of melting_heat.
    """
    value: value = value
    """
    value child of melting_heat.
    """
