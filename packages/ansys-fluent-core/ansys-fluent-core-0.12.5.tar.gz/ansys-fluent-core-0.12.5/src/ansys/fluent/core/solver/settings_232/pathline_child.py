#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .uid import uid
from .options_8 import options
from .range import range
from .style_attribute import style_attribute
from .accuracy_control_1 import accuracy_control
from .plot_1 import plot
from .step import step
from .skip import skip
from .coarsen_1 import coarsen
from .onzone import onzone
from .onphysics import onphysics
from .field import field
from .surfaces_list import surfaces_list
from .velocity_domain import velocity_domain
from .color_map import color_map
from .draw_mesh import draw_mesh
from .mesh_object import mesh_object
from .display_state_name import display_state_name
from .physics_1 import physics
from .geometry_4 import geometry
from .surfaces_1 import surfaces
from .axes import axes
from .curves import curves
from .display_2 import display
from .update_min_max import update_min_max
class pathline_child(Group):
    """
    'child_object_type' of pathline.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'range', 'style_attribute',
         'accuracy_control', 'plot', 'step', 'skip', 'coarsen', 'onzone',
         'onphysics', 'field', 'surfaces_list', 'velocity_domain',
         'color_map', 'draw_mesh', 'mesh_object', 'display_state_name',
         'physics', 'geometry', 'surfaces', 'axes', 'curves']

    name: name = name
    """
    name child of pathline_child.
    """
    uid: uid = uid
    """
    uid child of pathline_child.
    """
    options: options = options
    """
    options child of pathline_child.
    """
    range: range = range
    """
    range child of pathline_child.
    """
    style_attribute: style_attribute = style_attribute
    """
    style_attribute child of pathline_child.
    """
    accuracy_control: accuracy_control = accuracy_control
    """
    accuracy_control child of pathline_child.
    """
    plot: plot = plot
    """
    plot child of pathline_child.
    """
    step: step = step
    """
    step child of pathline_child.
    """
    skip: skip = skip
    """
    skip child of pathline_child.
    """
    coarsen: coarsen = coarsen
    """
    coarsen child of pathline_child.
    """
    onzone: onzone = onzone
    """
    onzone child of pathline_child.
    """
    onphysics: onphysics = onphysics
    """
    onphysics child of pathline_child.
    """
    field: field = field
    """
    field child of pathline_child.
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of pathline_child.
    """
    velocity_domain: velocity_domain = velocity_domain
    """
    velocity_domain child of pathline_child.
    """
    color_map: color_map = color_map
    """
    color_map child of pathline_child.
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of pathline_child.
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of pathline_child.
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of pathline_child.
    """
    physics: physics = physics
    """
    physics child of pathline_child.
    """
    geometry: geometry = geometry
    """
    geometry child of pathline_child.
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of pathline_child.
    """
    axes: axes = axes
    """
    axes child of pathline_child.
    """
    curves: curves = curves
    """
    curves child of pathline_child.
    """
    command_names = \
        ['display', 'update_min_max']

    display: display = display
    """
    display command of pathline_child.
    """
    update_min_max: update_min_max = update_min_max
    """
    update_min_max command of pathline_child.
    """
