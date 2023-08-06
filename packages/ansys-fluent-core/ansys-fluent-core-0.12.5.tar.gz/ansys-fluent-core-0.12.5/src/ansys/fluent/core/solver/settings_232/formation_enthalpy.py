#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class formation_enthalpy(Group):
    """
    'formation_enthalpy' child.
    """

    fluent_name = "formation-enthalpy"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of formation_enthalpy.
    """
    value: value = value
    """
    value child of formation_enthalpy.
    """
