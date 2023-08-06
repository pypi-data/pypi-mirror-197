#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_4 import enable
from .solution_method import solution_method
class do_energy_coupling(Group):
    """
    'do_energy_coupling' child.
    """

    fluent_name = "do-energy-coupling"

    child_names = \
        ['enable', 'solution_method']

    enable: enable = enable
    """
    enable child of do_energy_coupling.
    """
    solution_method: solution_method = solution_method
    """
    solution_method child of do_energy_coupling.
    """
