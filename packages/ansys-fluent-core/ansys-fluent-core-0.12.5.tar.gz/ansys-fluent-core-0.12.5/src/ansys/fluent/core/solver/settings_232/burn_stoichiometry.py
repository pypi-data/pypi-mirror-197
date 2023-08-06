#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class burn_stoichiometry(Group):
    """
    'burn_stoichiometry' child.
    """

    fluent_name = "burn-stoichiometry"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of burn_stoichiometry.
    """
    value: value = value
    """
    value child of burn_stoichiometry.
    """
