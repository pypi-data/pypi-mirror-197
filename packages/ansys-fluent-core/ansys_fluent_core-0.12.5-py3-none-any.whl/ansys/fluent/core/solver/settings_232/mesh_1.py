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
from .mesh_child import mesh_child

class mesh(NamedObject[mesh_child], _CreatableNamedObjectMixin[mesh_child]):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of mesh.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of mesh.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of mesh.
    """
    child_object_type: mesh_child = mesh_child
    """
    child_object_type of mesh.
    """
