#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .day import day
from .month import month
from .hour import hour
from .minute import minute
class date_and_time(Group):
    """
    'date_and_time' child.
    """

    fluent_name = "date-and-time"

    child_names = \
        ['day', 'month', 'hour', 'minute']

    day: day = day
    """
    day child of date_and_time.
    """
    month: month = month
    """
    month child of date_and_time.
    """
    hour: hour = hour
    """
    hour child of date_and_time.
    """
    minute: minute = minute
    """
    minute child of date_and_time.
    """
