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

class ablation_species_mf(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'ablation_species_mf' child.
    """

    fluent_name = "ablation-species-mf"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of ablation_species_mf.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of ablation_species_mf.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of ablation_species_mf.
    """
    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of ablation_species_mf.
    """
