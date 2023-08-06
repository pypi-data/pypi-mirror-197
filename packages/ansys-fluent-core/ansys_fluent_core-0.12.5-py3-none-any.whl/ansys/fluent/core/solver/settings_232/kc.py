#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .method_2 import method
from .number_of_coeff import number_of_coeff
from .function_of import function_of
from .coefficients_1 import coefficients
from .value_1 import value
from .piecewise_polynomial_1 import piecewise_polynomial
from .piecewise_linear import piecewise_linear
class kc(Group):
    """
    'kc' child.
    """

    fluent_name = "kc"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients', 'value',
         'piecewise_polynomial', 'piecewise_linear']

    method: method = method
    """
    method child of kc.
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of kc.
    """
    function_of: function_of = function_of
    """
    function_of child of kc.
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of kc.
    """
    value: value = value
    """
    value child of kc.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of kc.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of kc.
    """
