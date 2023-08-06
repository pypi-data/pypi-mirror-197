#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .background_2 import background
from .rendering import rendering
from .display_live_preview import display_live_preview
class raytracing_options(Group):
    """
    'raytracing_options' child.
    """

    fluent_name = "raytracing-options"

    child_names = \
        ['background', 'rendering']

    background: background = background
    """
    background child of raytracing_options.
    """
    rendering: rendering = rendering
    """
    rendering child of raytracing_options.
    """
    command_names = \
        ['display_live_preview']

    display_live_preview: display_live_preview = display_live_preview
    """
    display_live_preview command of raytracing_options.
    """
