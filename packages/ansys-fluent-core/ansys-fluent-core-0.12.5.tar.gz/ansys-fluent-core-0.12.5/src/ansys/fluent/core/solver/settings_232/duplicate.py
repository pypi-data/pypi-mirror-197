#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .from_ import from_
from .to import to
class duplicate(Command):
    """
    'duplicate' command.
    
    Parameters
    ----------
        from_ : str
            'from' child.
        to : str
            'to' child.
    
    """

    fluent_name = "duplicate"

    argument_names = \
        ['from_', 'to']

    from_: from_ = from_
    """
    from_ argument of duplicate.
    """
    to: to = to
    """
    to argument of duplicate.
    """
