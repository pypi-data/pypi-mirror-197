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
from .moment_child import moment_child

class moment(NamedObject[moment_child], _CreatableNamedObjectMixin[moment_child]):
    """
    'moment' child.
    """

    fluent_name = "moment"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of moment.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of moment.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of moment.
    """
    child_object_type: moment_child = moment_child
    """
    child_object_type of moment.
    """
