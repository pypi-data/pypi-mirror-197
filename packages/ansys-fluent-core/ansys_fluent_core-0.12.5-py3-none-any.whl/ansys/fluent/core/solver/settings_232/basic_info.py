#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .number_of_blades import number_of_blades
from .rotor_speed import rotor_speed
from .tip_radius import tip_radius
from .root_radius import root_radius
class basic_info(Group):
    """
    Menu to define the rotor basic informations:
    
     - Number of Blades 
     - Rotor Speed  , 
     - Tip Radius 
     - Root Radius , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "basic-info"

    child_names = \
        ['number_of_blades', 'rotor_speed', 'tip_radius', 'root_radius']

    number_of_blades: number_of_blades = number_of_blades
    """
    number_of_blades child of basic_info.
    """
    rotor_speed: rotor_speed = rotor_speed
    """
    rotor_speed child of basic_info.
    """
    tip_radius: tip_radius = tip_radius
    """
    tip_radius child of basic_info.
    """
    root_radius: root_radius = root_radius
    """
    root_radius child of basic_info.
    """
