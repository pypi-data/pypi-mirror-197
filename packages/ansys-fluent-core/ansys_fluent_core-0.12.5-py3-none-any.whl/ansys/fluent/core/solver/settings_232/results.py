#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .surfaces_2 import surfaces
from .graphics import graphics
from .plot_2 import plot
from .scene import scene
from .animations import animations
from .report_1 import report
class results(Group):
    """
    'results' child.
    """

    fluent_name = "results"

    child_names = \
        ['surfaces', 'graphics', 'plot', 'scene', 'animations', 'report']

    surfaces: surfaces = surfaces
    """
    surfaces child of results.
    """
    graphics: graphics = graphics
    """
    graphics child of results.
    """
    plot: plot = plot
    """
    plot child of results.
    """
    scene: scene = scene
    """
    scene child of results.
    """
    animations: animations = animations
    """
    animations child of results.
    """
    report: report = report
    """
    report child of results.
    """
