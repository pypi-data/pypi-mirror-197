#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list import list
from .list_properties import list_properties
from .duplicate import duplicate
from .copy import copy
from .list_beam_parameters import list_beam_parameters
from .beams_child import beams_child

class beams(NamedObject[beams_child], _CreatableNamedObjectMixin[beams_child]):
    """
    Enter the optical beams menu.
    """

    fluent_name = "beams"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'copy',
         'list_beam_parameters']

    list: list = list
    """
    list command of beams.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of beams.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of beams.
    """
    copy: copy = copy
    """
    copy command of beams.
    """
    list_beam_parameters: list_beam_parameters = list_beam_parameters
    """
    list_beam_parameters command of beams.
    """
    child_object_type: beams_child = beams_child
    """
    child_object_type of beams.
    """
