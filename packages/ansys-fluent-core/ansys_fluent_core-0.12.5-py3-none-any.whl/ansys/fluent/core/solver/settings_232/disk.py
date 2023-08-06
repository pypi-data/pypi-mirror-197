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
from .disk_child import disk_child

class disk(NamedObject[disk_child], _CreatableNamedObjectMixin[disk_child]):
    """
    Main menu to define a rotor disk:
    
     - delete : delete a vbm disk
     - edit   : edit a vbm disk
     - new    : create a new vbm disk
     - rename : rename a vbm disk.
    
    """

    fluent_name = "disk"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of disk.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of disk.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of disk.
    """
    child_object_type: disk_child = disk_child
    """
    child_object_type of disk.
    """
