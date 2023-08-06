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
from .mixture_child import mixture_child

class mixture(NamedObject[mixture_child], _CreatableNamedObjectMixin[mixture_child]):
    """
    'mixture' child.
    """

    fluent_name = "mixture"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of mixture.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of mixture.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of mixture.
    """
    child_object_type: mixture_child = mixture_child
    """
    child_object_type of mixture.
    """
