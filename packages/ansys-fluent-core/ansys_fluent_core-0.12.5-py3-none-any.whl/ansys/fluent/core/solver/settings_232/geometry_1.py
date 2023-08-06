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
from .geometry_child import geometry_child

class geometry(NamedObject[geometry_child], _CreatableNamedObjectMixin[geometry_child]):
    """
    Main menu to define a disk-section:
    
     - delete : delete a disk-section% - edit   : edit a disk-section
     - new    : create a new disk-section
     - rename : rename a vbm disk-section.
    
    """

    fluent_name = "geometry"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of geometry.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of geometry.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of geometry.
    """
    child_object_type: geometry_child = geometry_child
    """
    child_object_type of geometry.
    """
