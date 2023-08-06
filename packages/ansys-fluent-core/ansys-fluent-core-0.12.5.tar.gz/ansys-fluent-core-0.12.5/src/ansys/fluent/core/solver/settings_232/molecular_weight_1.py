#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class molecular_weight(Group):
    """
    'molecular_weight' child.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of molecular_weight.
    """
    value: value = value
    """
    value child of molecular_weight.
    """
