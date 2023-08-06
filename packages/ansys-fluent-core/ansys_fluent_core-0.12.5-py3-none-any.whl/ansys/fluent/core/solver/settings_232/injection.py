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
from .injection_child import injection_child

class injection(NamedObject[injection_child], _CreatableNamedObjectMixin[injection_child]):
    """
    'injection' child.
    """

    fluent_name = "injection"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of injection.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of injection.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of injection.
    """
    child_object_type: injection_child = injection_child
    """
    child_object_type of injection.
    """
