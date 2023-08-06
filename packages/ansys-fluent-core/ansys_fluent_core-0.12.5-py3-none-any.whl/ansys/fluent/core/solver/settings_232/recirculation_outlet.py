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
from .recirculation_outlet_child import recirculation_outlet_child

class recirculation_outlet(NamedObject[recirculation_outlet_child], _NonCreatableNamedObjectMixin[recirculation_outlet_child]):
    """
    'recirculation_outlet' child.
    """

    fluent_name = "recirculation-outlet"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of recirculation_outlet.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of recirculation_outlet.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of recirculation_outlet.
    """
    child_object_type: recirculation_outlet_child = recirculation_outlet_child
    """
    child_object_type of recirculation_outlet.
    """
