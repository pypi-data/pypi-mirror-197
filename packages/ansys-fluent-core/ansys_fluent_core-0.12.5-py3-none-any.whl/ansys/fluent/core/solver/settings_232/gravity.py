#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enable_2 import enable
from .components import components
from .gravity_mrf_behavior import gravity_mrf_behavior
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['enable', 'components', 'gravity_mrf_behavior']

    enable: enable = enable
    """
    enable child of gravity.
    """
    components: components = components
    """
    components child of gravity.
    """
    gravity_mrf_behavior: gravity_mrf_behavior = gravity_mrf_behavior
    """
    gravity_mrf_behavior child of gravity.
    """
