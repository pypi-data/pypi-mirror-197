#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .target_type import target_type
from .number_of_cells import number_of_cells
from .factor_of_cells import factor_of_cells
class target(Command):
    """
    Set the target type and value for anisotropic adaption.
    
    Parameters
    ----------
        target_type : str
            'target_type' child.
        number_of_cells : real
            'number_of_cells' child.
        factor_of_cells : real
            'factor_of_cells' child.
    
    """

    fluent_name = "target"

    argument_names = \
        ['target_type', 'number_of_cells', 'factor_of_cells']

    target_type: target_type = target_type
    """
    target_type argument of target.
    """
    number_of_cells: number_of_cells = number_of_cells
    """
    number_of_cells argument of target.
    """
    factor_of_cells: factor_of_cells = factor_of_cells
    """
    factor_of_cells argument of target.
    """
