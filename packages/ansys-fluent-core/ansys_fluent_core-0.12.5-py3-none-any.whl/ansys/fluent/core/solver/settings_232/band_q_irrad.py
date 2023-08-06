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
from .child_object_type_child_1 import child_object_type_child

class band_q_irrad(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'band_q_irrad' child.
    """

    fluent_name = "band-q-irrad"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of band_q_irrad.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of band_q_irrad.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of band_q_irrad.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of band_q_irrad.
    """
