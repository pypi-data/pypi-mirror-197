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
from .convergence_reports_child import convergence_reports_child

class convergence_reports(NamedObject[convergence_reports_child], _CreatableNamedObjectMixin[convergence_reports_child]):
    """
    'convergence_reports' child.
    """

    fluent_name = "convergence-reports"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    list: list = list
    """
    list command of convergence_reports.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of convergence_reports.
    """
    duplicate: duplicate = duplicate
    """
    duplicate command of convergence_reports.
    """
    child_object_type: convergence_reports_child = convergence_reports_child
    """
    child_object_type of convergence_reports.
    """
