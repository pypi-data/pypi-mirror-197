#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option import option
from .const_htc import const_htc
from .const_nu import const_nu
class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    child_names = \
        ['option', 'const_htc', 'const_nu']

    option: option = option
    """
    option child of heat_exchange.
    """
    const_htc: const_htc = const_htc
    """
    const_htc child of heat_exchange.
    """
    const_nu: const_nu = const_nu
    """
    const_nu child of heat_exchange.
    """
