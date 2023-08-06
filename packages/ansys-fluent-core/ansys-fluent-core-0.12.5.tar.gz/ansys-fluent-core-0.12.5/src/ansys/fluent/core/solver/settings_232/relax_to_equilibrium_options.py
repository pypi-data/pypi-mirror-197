#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .turbulent_rate_constant import turbulent_rate_constant
from .chemical_rate_constant import chemical_rate_constant
from .fuel_species import fuel_species
from .equilibrium_rich_flammability import equilibrium_rich_flammability
from .equilibrium_rich_flammability_options import equilibrium_rich_flammability_options
class relax_to_equilibrium_options(Group):
    """
    'relax_to_equilibrium_options' child.
    """

    fluent_name = "relax-to-equilibrium-options"

    child_names = \
        ['turbulent_rate_constant', 'chemical_rate_constant', 'fuel_species',
         'equilibrium_rich_flammability',
         'equilibrium_rich_flammability_options']

    turbulent_rate_constant: turbulent_rate_constant = turbulent_rate_constant
    """
    turbulent_rate_constant child of relax_to_equilibrium_options.
    """
    chemical_rate_constant: chemical_rate_constant = chemical_rate_constant
    """
    chemical_rate_constant child of relax_to_equilibrium_options.
    """
    fuel_species: fuel_species = fuel_species
    """
    fuel_species child of relax_to_equilibrium_options.
    """
    equilibrium_rich_flammability: equilibrium_rich_flammability = equilibrium_rich_flammability
    """
    equilibrium_rich_flammability child of relax_to_equilibrium_options.
    """
    equilibrium_rich_flammability_options: equilibrium_rich_flammability_options = equilibrium_rich_flammability_options
    """
    equilibrium_rich_flammability_options child of relax_to_equilibrium_options.
    """
