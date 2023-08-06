#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .latitude import latitude
from .longitude import longitude
from .timezone import timezone
from .north_direction import north_direction
from .east_direction import east_direction
from .date_and_time import date_and_time
from .calculator_method import calculator_method
from .sunshine_factor import sunshine_factor
class solar_calculator(Group):
    """
    'solar_calculator' child.
    """

    fluent_name = "solar-calculator"

    child_names = \
        ['latitude', 'longitude', 'timezone', 'north_direction',
         'east_direction', 'date_and_time', 'calculator_method',
         'sunshine_factor']

    latitude: latitude = latitude
    """
    latitude child of solar_calculator.
    """
    longitude: longitude = longitude
    """
    longitude child of solar_calculator.
    """
    timezone: timezone = timezone
    """
    timezone child of solar_calculator.
    """
    north_direction: north_direction = north_direction
    """
    north_direction child of solar_calculator.
    """
    east_direction: east_direction = east_direction
    """
    east_direction child of solar_calculator.
    """
    date_and_time: date_and_time = date_and_time
    """
    date_and_time child of solar_calculator.
    """
    calculator_method: calculator_method = calculator_method
    """
    calculator_method child of solar_calculator.
    """
    sunshine_factor: sunshine_factor = sunshine_factor
    """
    sunshine_factor child of solar_calculator.
    """
