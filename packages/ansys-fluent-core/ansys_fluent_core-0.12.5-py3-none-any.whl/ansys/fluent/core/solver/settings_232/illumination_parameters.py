#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .direct_solar_irradiation import direct_solar_irradiation
from .diffuse_solar_irradiation import diffuse_solar_irradiation
from .spectral_fraction import spectral_fraction
class illumination_parameters(Group):
    """
    'illumination_parameters' child.
    """

    fluent_name = "illumination-parameters"

    child_names = \
        ['direct_solar_irradiation', 'diffuse_solar_irradiation',
         'spectral_fraction']

    direct_solar_irradiation: direct_solar_irradiation = direct_solar_irradiation
    """
    direct_solar_irradiation child of illumination_parameters.
    """
    diffuse_solar_irradiation: diffuse_solar_irradiation = diffuse_solar_irradiation
    """
    diffuse_solar_irradiation child of illumination_parameters.
    """
    spectral_fraction: spectral_fraction = spectral_fraction
    """
    spectral_fraction child of illumination_parameters.
    """
