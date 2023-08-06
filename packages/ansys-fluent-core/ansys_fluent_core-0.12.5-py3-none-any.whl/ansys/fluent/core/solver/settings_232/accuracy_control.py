#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_4 import option
from .tolerance import tolerance
from .max_number_of_refinements import max_number_of_refinements
from .number_of_cells_to_cross import number_of_cells_to_cross
class accuracy_control(Group):
    """
    'accuracy_control' child.
    """

    fluent_name = "accuracy-control"

    child_names = \
        ['option', 'tolerance', 'max_number_of_refinements',
         'number_of_cells_to_cross']

    option: option = option
    """
    option child of accuracy_control.
    """
    tolerance: tolerance = tolerance
    """
    tolerance child of accuracy_control.
    """
    max_number_of_refinements: max_number_of_refinements = max_number_of_refinements
    """
    max_number_of_refinements child of accuracy_control.
    """
    number_of_cells_to_cross: number_of_cells_to_cross = number_of_cells_to_cross
    """
    number_of_cells_to_cross child of accuracy_control.
    """
