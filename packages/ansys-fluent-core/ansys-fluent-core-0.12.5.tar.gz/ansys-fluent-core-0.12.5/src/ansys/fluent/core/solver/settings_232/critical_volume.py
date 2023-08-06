#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class critical_volume(Group):
    """
    'critical_volume' child.
    """

    fluent_name = "critical-volume"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of critical_volume.
    """
    value: value = value
    """
    value child of critical_volume.
    """
