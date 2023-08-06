#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option import option
from .constant import constant
from .piecewise_linear import piecewise_linear
from .polynomial import polynomial
from .user_defined_2 import user_defined
class diffuse_solar_irradiation(Group):
    """
    'diffuse_solar_irradiation' child.
    """

    fluent_name = "diffuse-solar-irradiation"

    child_names = \
        ['option', 'constant', 'piecewise_linear', 'polynomial',
         'user_defined']

    option: option = option
    """
    option child of diffuse_solar_irradiation.
    """
    constant: constant = constant
    """
    constant child of diffuse_solar_irradiation.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of diffuse_solar_irradiation.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of diffuse_solar_irradiation.
    """
    user_defined: user_defined = user_defined
    """
    user_defined child of diffuse_solar_irradiation.
    """
