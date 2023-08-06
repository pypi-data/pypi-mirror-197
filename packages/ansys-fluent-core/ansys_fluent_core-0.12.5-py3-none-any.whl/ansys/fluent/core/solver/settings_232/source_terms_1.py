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
from .source_terms_child import source_terms_child

class source_terms(NamedObject[source_terms_child], _NonCreatableNamedObjectMixin[source_terms_child]):
    """
    'source_terms' child.
    """

    fluent_name = "source-terms"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of source_terms.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of source_terms.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of source_terms.
    """
    child_object_type: source_terms_child = source_terms_child
    """
    child_object_type of source_terms.
    """
