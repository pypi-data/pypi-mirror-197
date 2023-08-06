#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .diameter import diameter
from .diameter_2 import diameter_2
from .option import option
from .rosin_rammler_settings import rosin_rammler_settings
from .tabulated_size_settings import tabulated_size_settings
class particle_size(Group):
    """
    'particle_size' child.
    """

    fluent_name = "particle-size"

    child_names = \
        ['diameter', 'diameter_2', 'option', 'rosin_rammler_settings',
         'tabulated_size_settings']

    diameter: diameter = diameter
    """
    diameter child of particle_size.
    """
    diameter_2: diameter_2 = diameter_2
    """
    diameter_2 child of particle_size.
    """
    option: option = option
    """
    option child of particle_size.
    """
    rosin_rammler_settings: rosin_rammler_settings = rosin_rammler_settings
    """
    rosin_rammler_settings child of particle_size.
    """
    tabulated_size_settings: tabulated_size_settings = tabulated_size_settings
    """
    tabulated_size_settings child of particle_size.
    """
