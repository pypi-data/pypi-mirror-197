#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .dynamic_stress import dynamic_stress
from .dynamic_energy_flux import dynamic_energy_flux
from .dynamic_scalar_flux import dynamic_scalar_flux
from .subgrid_dynamic_fvar import subgrid_dynamic_fvar
from .cvreman import cvreman
from .wall_model import wall_model
from .cw1 import cw1
from .cw2 import cw2
class les_model_options(Group):
    """
    'les_model_options' child.
    """

    fluent_name = "les-model-options"

    child_names = \
        ['dynamic_stress', 'dynamic_energy_flux', 'dynamic_scalar_flux',
         'subgrid_dynamic_fvar', 'cvreman', 'wall_model', 'cw1', 'cw2']

    dynamic_stress: dynamic_stress = dynamic_stress
    """
    dynamic_stress child of les_model_options.
    """
    dynamic_energy_flux: dynamic_energy_flux = dynamic_energy_flux
    """
    dynamic_energy_flux child of les_model_options.
    """
    dynamic_scalar_flux: dynamic_scalar_flux = dynamic_scalar_flux
    """
    dynamic_scalar_flux child of les_model_options.
    """
    subgrid_dynamic_fvar: subgrid_dynamic_fvar = subgrid_dynamic_fvar
    """
    subgrid_dynamic_fvar child of les_model_options.
    """
    cvreman: cvreman = cvreman
    """
    cvreman child of les_model_options.
    """
    wall_model: wall_model = wall_model
    """
    wall_model child of les_model_options.
    """
    cw1: cw1 = cw1
    """
    cw1 child of les_model_options.
    """
    cw2: cw2 = cw2
    """
    cw2 child of les_model_options.
    """
