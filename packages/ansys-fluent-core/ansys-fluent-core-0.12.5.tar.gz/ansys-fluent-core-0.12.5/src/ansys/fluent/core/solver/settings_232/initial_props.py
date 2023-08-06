#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .location import location
from .matrix import matrix
from .cone_settings import cone_settings
from .velocity import velocity
from .angular_velocity import angular_velocity
from .mass_flow_rate import mass_flow_rate
from .times import times
from .particle_size import particle_size
from .temperature import temperature
from .temperature_2 import temperature_2
class initial_props(Group):
    """
    'initial_props' child.
    """

    fluent_name = "initial-props"

    child_names = \
        ['location', 'matrix', 'cone_settings', 'velocity',
         'angular_velocity', 'mass_flow_rate', 'times', 'particle_size',
         'temperature', 'temperature_2']

    location: location = location
    """
    location child of initial_props.
    """
    matrix: matrix = matrix
    """
    matrix child of initial_props.
    """
    cone_settings: cone_settings = cone_settings
    """
    cone_settings child of initial_props.
    """
    velocity: velocity = velocity
    """
    velocity child of initial_props.
    """
    angular_velocity: angular_velocity = angular_velocity
    """
    angular_velocity child of initial_props.
    """
    mass_flow_rate: mass_flow_rate = mass_flow_rate
    """
    mass_flow_rate child of initial_props.
    """
    times: times = times
    """
    times child of initial_props.
    """
    particle_size: particle_size = particle_size
    """
    particle_size child of initial_props.
    """
    temperature: temperature = temperature
    """
    temperature child of initial_props.
    """
    temperature_2: temperature_2 = temperature_2
    """
    temperature_2 child of initial_props.
    """
