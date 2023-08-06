#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_2 import name
from .register import register
from .frequency_2 import frequency
from .active_1 import active
from .verbosity_6 import verbosity
class register_based_child(Group):
    """
    'child_object_type' of register_based.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity']

    name: name = name
    """
    name child of register_based_child.
    """
    register: register = register
    """
    register child of register_based_child.
    """
    frequency: frequency = frequency
    """
    frequency child of register_based_child.
    """
    active: active = active
    """
    active child of register_based_child.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of register_based_child.
    """
