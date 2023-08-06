#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class latent_heat(Group):
    """
    'latent_heat' child.
    """

    fluent_name = "latent-heat"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of latent_heat.
    """
    value: value = value
    """
    value child of latent_heat.
    """
