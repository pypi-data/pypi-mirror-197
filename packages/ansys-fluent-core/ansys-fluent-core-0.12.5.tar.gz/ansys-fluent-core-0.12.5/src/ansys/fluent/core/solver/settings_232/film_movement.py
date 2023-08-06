#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .condensing_film import condensing_film
from .all_film import all_film
class film_movement(Group):
    """
    'film_movement' child.
    """

    fluent_name = "film-movement"

    child_names = \
        ['condensing_film', 'all_film']

    condensing_film: condensing_film = condensing_film
    """
    condensing_film child of film_movement.
    """
    all_film: all_film = all_film
    """
    all_film child of film_movement.
    """
