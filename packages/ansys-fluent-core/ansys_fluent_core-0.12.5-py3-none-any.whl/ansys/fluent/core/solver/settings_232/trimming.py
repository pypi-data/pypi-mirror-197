#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .trim_option import trim_option
from .update_frequency import update_frequency
from .damping_factor import damping_factor
from .thrust_coef import thrust_coef
from .pitch_moment_coef import pitch_moment_coef
from .roll_moment_coef import roll_moment_coef
class trimming(Group):
    """
    Menu to define rotor trimming set-up.
    
     - trim-option       : to define collective and cyclic pitches to trim, 
     - update-frequency  : the number of solver iterations that pitch angle will be updated each time, 
     - damping-factor    : relaxation factor for pitch angles, 
     - thrust-coef       : desired thrust coefficient to set pitch for
     - pitch-moment-coef : desired pitch-moment coefficient to set pitch for, 
     - roll-moment-coef  : desired roll-moment coefficient to set pitch for, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "trimming"

    child_names = \
        ['trim_option', 'update_frequency', 'damping_factor', 'thrust_coef',
         'pitch_moment_coef', 'roll_moment_coef']

    trim_option: trim_option = trim_option
    """
    trim_option child of trimming.
    """
    update_frequency: update_frequency = update_frequency
    """
    update_frequency child of trimming.
    """
    damping_factor: damping_factor = damping_factor
    """
    damping_factor child of trimming.
    """
    thrust_coef: thrust_coef = thrust_coef
    """
    thrust_coef child of trimming.
    """
    pitch_moment_coef: pitch_moment_coef = pitch_moment_coef
    """
    pitch_moment_coef child of trimming.
    """
    roll_moment_coef: roll_moment_coef = roll_moment_coef
    """
    roll_moment_coef child of trimming.
    """
