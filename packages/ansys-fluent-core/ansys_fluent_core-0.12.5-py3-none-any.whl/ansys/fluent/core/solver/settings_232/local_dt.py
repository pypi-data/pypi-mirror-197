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

class local_dt(NamedObject[local_dt_child], _NonCreatableNamedObjectMixin[local_dt_child]):
    """
    'local_dt' child.
    """

    fluent_name = "local-dt"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of local_dt.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of local_dt.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of local_dt.
    """
    child_object_type: local_dt_child = local_dt_child
    """
    child_object_type of local_dt.
    """
