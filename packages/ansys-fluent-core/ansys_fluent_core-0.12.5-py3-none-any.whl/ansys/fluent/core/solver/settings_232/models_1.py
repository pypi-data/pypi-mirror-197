#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .multiphase import multiphase
from .energy import energy
from .viscous import viscous
from .radiation import radiation
from .species import species
from .discrete_phase import discrete_phase
from .virtual_blade_model import virtual_blade_model
from .optics import optics
from .structure import structure
from .ablation import ablation
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['multiphase', 'energy', 'viscous', 'radiation', 'species',
         'discrete_phase', 'virtual_blade_model', 'optics', 'structure',
         'ablation']

    multiphase: multiphase = multiphase
    """
    multiphase child of models.
    """
    energy: energy = energy
    """
    energy child of models.
    """
    viscous: viscous = viscous
    """
    viscous child of models.
    """
    radiation: radiation = radiation
    """
    radiation child of models.
    """
    species: species = species
    """
    species child of models.
    """
    discrete_phase: discrete_phase = discrete_phase
    """
    discrete_phase child of models.
    """
    virtual_blade_model: virtual_blade_model = virtual_blade_model
    """
    virtual_blade_model child of models.
    """
    optics: optics = optics
    """
    optics child of models.
    """
    structure: structure = structure
    """
    structure child of models.
    """
    ablation: ablation = ablation
    """
    ablation child of models.
    """
