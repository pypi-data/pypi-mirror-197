#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class shear_modulus_02(Group):
    """
    'shear_modulus_02' child.
    """

    fluent_name = "shear-modulus-02"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of shear_modulus_02.
    """
    value: value = value
    """
    value child of shear_modulus_02.
    """
