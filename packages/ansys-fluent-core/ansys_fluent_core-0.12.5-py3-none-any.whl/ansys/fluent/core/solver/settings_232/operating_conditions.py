#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .gravity import gravity
from .real_gas_state import real_gas_state
from .operating_pressure import operating_pressure
from .reference_pressure_location import reference_pressure_location
from .reference_pressure_method import reference_pressure_method
from .operating_density import operating_density
from .operating_temperature import operating_temperature
from .used_ref_pressure_location import used_ref_pressure_location
from .use_inlet_temperature_for_operating_density import use_inlet_temperature_for_operating_density
class operating_conditions(Group):
    """
    'operating_conditions' child.
    """

    fluent_name = "operating-conditions"

    child_names = \
        ['gravity', 'real_gas_state', 'operating_pressure',
         'reference_pressure_location', 'reference_pressure_method',
         'operating_density', 'operating_temperature']

    gravity: gravity = gravity
    """
    gravity child of operating_conditions.
    """
    real_gas_state: real_gas_state = real_gas_state
    """
    real_gas_state child of operating_conditions.
    """
    operating_pressure: operating_pressure = operating_pressure
    """
    operating_pressure child of operating_conditions.
    """
    reference_pressure_location: reference_pressure_location = reference_pressure_location
    """
    reference_pressure_location child of operating_conditions.
    """
    reference_pressure_method: reference_pressure_method = reference_pressure_method
    """
    reference_pressure_method child of operating_conditions.
    """
    operating_density: operating_density = operating_density
    """
    operating_density child of operating_conditions.
    """
    operating_temperature: operating_temperature = operating_temperature
    """
    operating_temperature child of operating_conditions.
    """
    command_names = \
        ['used_ref_pressure_location',
         'use_inlet_temperature_for_operating_density']

    used_ref_pressure_location: used_ref_pressure_location = used_ref_pressure_location
    """
    used_ref_pressure_location command of operating_conditions.
    """
    use_inlet_temperature_for_operating_density: use_inlet_temperature_for_operating_density = use_inlet_temperature_for_operating_density
    """
    use_inlet_temperature_for_operating_density command of operating_conditions.
    """
