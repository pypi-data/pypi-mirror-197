#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_10 import option
from .value_1 import value
class solut_exp_coeff(Group):
    """
    'solut_exp_coeff' child.
    """

    fluent_name = "solut-exp-coeff"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of solut_exp_coeff.
    """
    value: value = value
    """
    value child of solut_exp_coeff.
    """
