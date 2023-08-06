#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .solar_model import solar_model
from .sun_direction_vector import sun_direction_vector
from .illumination_parameters import illumination_parameters
from .quad_tree_parameters import quad_tree_parameters
from .ground_reflectivity import ground_reflectivity
from .scattering_fraction import scattering_fraction
from .solar_on_adjacent_fluid import solar_on_adjacent_fluid
from .direction_from_solar_calculator import direction_from_solar_calculator
from .solar_load_frequency import solar_load_frequency
from .solar_calculator import solar_calculator
from .apply_full_solar_irradiation import apply_full_solar_irradiation
from .autoread_solar_data import autoread_solar_data
from .autosave_solar_data import autosave_solar_data
from .solar_on_demand import solar_on_demand
class solar_load(Group):
    """
    'solar_load' child.
    """

    fluent_name = "solar-load"

    child_names = \
        ['solar_model', 'sun_direction_vector', 'illumination_parameters',
         'quad_tree_parameters', 'ground_reflectivity', 'scattering_fraction',
         'solar_on_adjacent_fluid', 'direction_from_solar_calculator',
         'solar_load_frequency', 'solar_calculator',
         'apply_full_solar_irradiation', 'autoread_solar_data',
         'autosave_solar_data']

    solar_model: solar_model = solar_model
    """
    solar_model child of solar_load.
    """
    sun_direction_vector: sun_direction_vector = sun_direction_vector
    """
    sun_direction_vector child of solar_load.
    """
    illumination_parameters: illumination_parameters = illumination_parameters
    """
    illumination_parameters child of solar_load.
    """
    quad_tree_parameters: quad_tree_parameters = quad_tree_parameters
    """
    quad_tree_parameters child of solar_load.
    """
    ground_reflectivity: ground_reflectivity = ground_reflectivity
    """
    ground_reflectivity child of solar_load.
    """
    scattering_fraction: scattering_fraction = scattering_fraction
    """
    scattering_fraction child of solar_load.
    """
    solar_on_adjacent_fluid: solar_on_adjacent_fluid = solar_on_adjacent_fluid
    """
    solar_on_adjacent_fluid child of solar_load.
    """
    direction_from_solar_calculator: direction_from_solar_calculator = direction_from_solar_calculator
    """
    direction_from_solar_calculator child of solar_load.
    """
    solar_load_frequency: solar_load_frequency = solar_load_frequency
    """
    solar_load_frequency child of solar_load.
    """
    solar_calculator: solar_calculator = solar_calculator
    """
    solar_calculator child of solar_load.
    """
    apply_full_solar_irradiation: apply_full_solar_irradiation = apply_full_solar_irradiation
    """
    apply_full_solar_irradiation child of solar_load.
    """
    autoread_solar_data: autoread_solar_data = autoread_solar_data
    """
    autoread_solar_data child of solar_load.
    """
    autosave_solar_data: autosave_solar_data = autosave_solar_data
    """
    autosave_solar_data child of solar_load.
    """
    command_names = \
        ['solar_on_demand']

    solar_on_demand: solar_on_demand = solar_on_demand
    """
    solar_on_demand command of solar_load.
    """
