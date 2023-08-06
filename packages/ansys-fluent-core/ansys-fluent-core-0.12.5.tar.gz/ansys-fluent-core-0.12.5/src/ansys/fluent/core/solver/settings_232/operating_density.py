#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_3 import enable
from .method import method
from .value import value
from .print_1 import print
class operating_density(Group):
    """
    Enable/disable use of a specified operating density.
    """

    fluent_name = "operating-density"

    child_names = \
        ['enable', 'method', 'value']

    enable: enable = enable
    """
    enable child of operating_density.
    """
    method: method = method
    """
    method child of operating_density.
    """
    value: value = value
    """
    value child of operating_density.
    """
    command_names = \
        ['print']

    print: print = print
    """
    print command of operating_density.
    """
