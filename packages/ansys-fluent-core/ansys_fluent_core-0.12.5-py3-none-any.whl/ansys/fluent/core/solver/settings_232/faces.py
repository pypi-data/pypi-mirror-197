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
from .list_face import list_face
from .faces_child import faces_child

class faces(NamedObject[faces_child], _CreatableNamedObjectMixin[faces_child]):
    """
    'faces' child.
    """

    fluent_name = "faces"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'list_face']

    list: list = list
    """
    list command of faces.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of faces.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of faces.
    """
    list_face: list_face = list_face
    """
    list_face command of faces.
    """
    child_object_type: faces_child = faces_child
    """
    child_object_type of faces.
    """
