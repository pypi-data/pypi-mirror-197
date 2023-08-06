#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .indicator_type import indicator_type
from .single_scalar_fn import single_scalar_fn
from .multi_scalar_fn import multi_scalar_fn
class indicator(Command):
    """
    Set the indicator type and variable(s) for anisotropic adaption.
    
    Parameters
    ----------
        indicator_type : str
            'indicator_type' child.
        single_scalar_fn : str
            'single_scalar_fn' child.
        multi_scalar_fn : typing.List[str]
            'multi_scalar_fn' child.
    
    """

    fluent_name = "indicator"

    argument_names = \
        ['indicator_type', 'single_scalar_fn', 'multi_scalar_fn']

    indicator_type: indicator_type = indicator_type
    """
    indicator_type argument of indicator.
    """
    single_scalar_fn: single_scalar_fn = single_scalar_fn
    """
    single_scalar_fn argument of indicator.
    """
    multi_scalar_fn: multi_scalar_fn = multi_scalar_fn
    """
    multi_scalar_fn argument of indicator.
    """
