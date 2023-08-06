#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .quality_1 import quality
from .denoiser import denoiser
from .thread_count import thread_count
from .max_rendering_timeout import max_rendering_timeout
class rendering(Group):
    """
    Enter the menu for rendering options.
    """

    fluent_name = "rendering"

    child_names = \
        ['quality', 'denoiser', 'thread_count', 'max_rendering_timeout']

    quality: quality = quality
    """
    quality child of rendering.
    """
    denoiser: denoiser = denoiser
    """
    denoiser child of rendering.
    """
    thread_count: thread_count = thread_count
    """
    thread_count child of rendering.
    """
    max_rendering_timeout: max_rendering_timeout = max_rendering_timeout
    """
    max_rendering_timeout child of rendering.
    """
