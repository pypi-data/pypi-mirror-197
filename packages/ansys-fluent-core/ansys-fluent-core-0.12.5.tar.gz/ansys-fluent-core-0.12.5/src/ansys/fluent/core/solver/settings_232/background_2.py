#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .hide_environment_keep_effects import hide_environment_keep_effects
from .environment_image import environment_image
from .latitude_1 import latitude
from .longitude_1 import longitude
from .view_zoom import view_zoom
from .show_backplate import show_backplate
from .backplate_color import backplate_color
from .backplate_image import backplate_image
class background(Group):
    """
    Enter the menu for background options.
    """

    fluent_name = "background"

    child_names = \
        ['hide_environment_keep_effects', 'environment_image', 'latitude',
         'longitude', 'view_zoom', 'show_backplate', 'backplate_color',
         'backplate_image']

    hide_environment_keep_effects: hide_environment_keep_effects = hide_environment_keep_effects
    """
    hide_environment_keep_effects child of background.
    """
    environment_image: environment_image = environment_image
    """
    environment_image child of background.
    """
    latitude: latitude = latitude
    """
    latitude child of background.
    """
    longitude: longitude = longitude
    """
    longitude child of background.
    """
    view_zoom: view_zoom = view_zoom
    """
    view_zoom child of background.
    """
    show_backplate: show_backplate = show_backplate
    """
    show_backplate child of background.
    """
    backplate_color: backplate_color = backplate_color
    """
    backplate_color child of background.
    """
    backplate_image: backplate_image = backplate_image
    """
    backplate_image child of background.
    """
