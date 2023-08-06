#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list import list
from .list_properties import list_properties
from .duplicate_2 import duplicate
from .create_1 import create_1
from .load_case_data import load_case_data
from .set_as_current_1 import set_as_current
from .delete_design_points import delete_design_points
from .save_journals import save_journals
from .clear_generated_data import clear_generated_data
from .update_current import update_current
from .update_all import update_all
from .update_selected import update_selected
from .design_points_child import design_points_child

class design_points(NamedObject[design_points_child], _CreatableNamedObjectMixin[design_points_child]):
    """
    'design_points' child.
    """

    fluent_name = "design-points"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'create_1', 'load_case_data',
         'set_as_current', 'delete_design_points', 'save_journals',
         'clear_generated_data', 'update_current', 'update_all',
         'update_selected']

    list: list = list
    """
    list command of design_points.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of design_points.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of design_points.
    """
    create_1: create_1 = create_1
    """
    create_1 command of design_points.
    """
    load_case_data: load_case_data = load_case_data
    """
    load_case_data command of design_points.
    """
    set_as_current: set_as_current = set_as_current
    """
    set_as_current command of design_points.
    """
    delete_design_points: delete_design_points = delete_design_points
    """
    delete_design_points command of design_points.
    """
    save_journals: save_journals = save_journals
    """
    save_journals command of design_points.
    """
    clear_generated_data: clear_generated_data = clear_generated_data
    """
    clear_generated_data command of design_points.
    """
    update_current: update_current = update_current
    """
    update_current command of design_points.
    """
    update_all: update_all = update_all
    """
    update_all command of design_points.
    """
    update_selected: update_selected = update_selected
    """
    update_selected command of design_points.
    """
    child_object_type: design_points_child = design_points_child
    """
    child_object_type of design_points.
    """
