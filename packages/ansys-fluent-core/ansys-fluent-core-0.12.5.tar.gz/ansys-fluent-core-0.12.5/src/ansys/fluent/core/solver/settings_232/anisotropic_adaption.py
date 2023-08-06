#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .operations import operations
from .iterations import iterations
from .fixed_zones import fixed_zones
from .adapt_mesh_1 import adapt_mesh
from .indicator import indicator
from .target import target
class anisotropic_adaption(Group):
    """
    'anisotropic_adaption' child.
    """

    fluent_name = "anisotropic-adaption"

    child_names = \
        ['operations', 'iterations', 'fixed_zones']

    operations: operations = operations
    """
    operations child of anisotropic_adaption.
    """
    iterations: iterations = iterations
    """
    iterations child of anisotropic_adaption.
    """
    fixed_zones: fixed_zones = fixed_zones
    """
    fixed_zones child of anisotropic_adaption.
    """
    command_names = \
        ['adapt_mesh', 'indicator', 'target']

    adapt_mesh: adapt_mesh = adapt_mesh
    """
    adapt_mesh command of anisotropic_adaption.
    """
    indicator: indicator = indicator
    """
    indicator command of anisotropic_adaption.
    """
    target: target = target
    """
    target command of anisotropic_adaption.
    """
