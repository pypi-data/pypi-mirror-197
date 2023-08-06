#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .model_1 import model
from .solar_load import solar_load
from .discrete_ordinates import discrete_ordinates
from .monte_carlo import monte_carlo
from .s2s import s2s
from .multiband import multiband
from .solve_frequency import solve_frequency
class radiation(Group):
    """
    'radiation' child.
    """

    fluent_name = "radiation"

    child_names = \
        ['model', 'solar_load', 'discrete_ordinates', 'monte_carlo', 's2s',
         'multiband', 'solve_frequency']

    model: model = model
    """
    model child of radiation.
    """
    solar_load: solar_load = solar_load
    """
    solar_load child of radiation.
    """
    discrete_ordinates: discrete_ordinates = discrete_ordinates
    """
    discrete_ordinates child of radiation.
    """
    monte_carlo: monte_carlo = monte_carlo
    """
    monte_carlo child of radiation.
    """
    s2s: s2s = s2s
    """
    s2s child of radiation.
    """
    multiband: multiband = multiband
    """
    multiband child of radiation.
    """
    solve_frequency: solve_frequency = solve_frequency
    """
    solve_frequency child of radiation.
    """
