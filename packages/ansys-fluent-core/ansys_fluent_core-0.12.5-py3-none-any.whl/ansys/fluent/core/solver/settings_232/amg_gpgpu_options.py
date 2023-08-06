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
from .amg_gpgpu_options_child import amg_gpgpu_options_child

class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child], _NonCreatableNamedObjectMixin[amg_gpgpu_options_child]):
    """
    'amg_gpgpu_options' child.
    """

    fluent_name = "amg-gpgpu-options"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of amg_gpgpu_options.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of amg_gpgpu_options.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of amg_gpgpu_options.
    """
    child_object_type: amg_gpgpu_options_child = amg_gpgpu_options_child
    """
    child_object_type of amg_gpgpu_options.
    """
