#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .io_mode import io_mode
from .compression_level import compression_level
from .single_precision_data import single_precision_data
class cffio_options(Group):
    """
    CFF I/O options.
    """

    fluent_name = "cffio-options"

    child_names = \
        ['io_mode', 'compression_level', 'single_precision_data']

    io_mode: io_mode = io_mode
    """
    io_mode child of cffio_options.
    """
    compression_level: compression_level = compression_level
    """
    compression_level child of cffio_options.
    """
    single_precision_data: single_precision_data = single_precision_data
    """
    single_precision_data child of cffio_options.
    """
