#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .a import a
from .b import b
from .c import c
class gupta_curve_fit_viscosity(Group):
    """
    'gupta_curve_fit_viscosity' child.
    """

    fluent_name = "gupta-curve-fit-viscosity"

    child_names = \
        ['a', 'b', 'c']

    a: a = a
    """
    a child of gupta_curve_fit_viscosity.
    """
    b: b = b
    """
    b child of gupta_curve_fit_viscosity.
    """
    c: c = c
    """
    c child of gupta_curve_fit_viscosity.
    """
