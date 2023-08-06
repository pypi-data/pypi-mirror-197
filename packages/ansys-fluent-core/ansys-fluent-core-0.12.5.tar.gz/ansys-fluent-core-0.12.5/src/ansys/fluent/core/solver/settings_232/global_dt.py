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
from .local_dt_child import local_dt_child

class global_dt(NamedObject[local_dt_child], _NonCreatableNamedObjectMixin[local_dt_child]):
    """
    'global_dt' child.
    """

    fluent_name = "global-dt"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of global_dt.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of global_dt.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of global_dt.
    """
    child_object_type: local_dt_child = local_dt_child
    """
    child_object_type of global_dt.
    """
