#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .basis import basis
from .method_1 import method
from .surfaces import surfaces
from .smoothing import smoothing
from .resolution import resolution
from .separation import separation
from .subdivide import subdivide
from .non_participating_zone_temperature import non_participating_zone_temperature
class viewfactor_settings(Group):
    """
    Enter viewfactor related settings.
    """

    fluent_name = "viewfactor-settings"

    child_names = \
        ['basis', 'method', 'surfaces', 'smoothing', 'resolution',
         'separation', 'subdivide', 'non_participating_zone_temperature']

    basis: basis = basis
    """
    basis child of viewfactor_settings.
    """
    method: method = method
    """
    method child of viewfactor_settings.
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of viewfactor_settings.
    """
    smoothing: smoothing = smoothing
    """
    smoothing child of viewfactor_settings.
    """
    resolution: resolution = resolution
    """
    resolution child of viewfactor_settings.
    """
    separation: separation = separation
    """
    separation child of viewfactor_settings.
    """
    subdivide: subdivide = subdivide
    """
    subdivide child of viewfactor_settings.
    """
    non_participating_zone_temperature: non_participating_zone_temperature = non_participating_zone_temperature
    """
    non_participating_zone_temperature child of viewfactor_settings.
    """
