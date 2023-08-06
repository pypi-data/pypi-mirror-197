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
from .interior_child import interior_child

class interior(NamedObject[interior_child], _NonCreatableNamedObjectMixin[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of interior.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of interior.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of interior.
    """
    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
