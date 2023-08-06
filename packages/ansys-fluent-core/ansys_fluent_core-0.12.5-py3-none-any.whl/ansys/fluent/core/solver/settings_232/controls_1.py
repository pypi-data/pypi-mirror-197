#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .courant_number import courant_number
from .p_v_controls import p_v_controls
from .relaxation_factor_1 import relaxation_factor
from .under_relaxation_1 import under_relaxation
from .pseudo_time_method_local_time_step import pseudo_time_method_local_time_step
from .pseudo_time_explicit_relaxation_factor import pseudo_time_explicit_relaxation_factor
from .acoustics_wave_eqn_controls import acoustics_wave_eqn_controls
from .contact_solution_controls import contact_solution_controls
from .equations import equations
from .limits import limits
from .advanced import advanced
from .reset_solution_controls import reset_solution_controls
from .reset_amg_controls import reset_amg_controls
from .reset_multi_stage_parameters import reset_multi_stage_parameters
from .reset_limits import reset_limits
from .reset_pseudo_time_method_generic import reset_pseudo_time_method_generic
from .reset_pseudo_time_method_equations import reset_pseudo_time_method_equations
from .reset_pseudo_time_method_relaxations import reset_pseudo_time_method_relaxations
from .reset_pseudo_time_method_scale_factors import reset_pseudo_time_method_scale_factors
class controls(Group):
    """
    'controls' child.
    """

    fluent_name = "controls"

    child_names = \
        ['courant_number', 'p_v_controls', 'relaxation_factor',
         'under_relaxation', 'pseudo_time_method_local_time_step',
         'pseudo_time_explicit_relaxation_factor',
         'acoustics_wave_eqn_controls', 'contact_solution_controls',
         'equations', 'limits', 'advanced']

    courant_number: courant_number = courant_number
    """
    courant_number child of controls.
    """
    p_v_controls: p_v_controls = p_v_controls
    """
    p_v_controls child of controls.
    """
    relaxation_factor: relaxation_factor = relaxation_factor
    """
    relaxation_factor child of controls.
    """
    under_relaxation: under_relaxation = under_relaxation
    """
    under_relaxation child of controls.
    """
    pseudo_time_method_local_time_step: pseudo_time_method_local_time_step = pseudo_time_method_local_time_step
    """
    pseudo_time_method_local_time_step child of controls.
    """
    pseudo_time_explicit_relaxation_factor: pseudo_time_explicit_relaxation_factor = pseudo_time_explicit_relaxation_factor
    """
    pseudo_time_explicit_relaxation_factor child of controls.
    """
    acoustics_wave_eqn_controls: acoustics_wave_eqn_controls = acoustics_wave_eqn_controls
    """
    acoustics_wave_eqn_controls child of controls.
    """
    contact_solution_controls: contact_solution_controls = contact_solution_controls
    """
    contact_solution_controls child of controls.
    """
    equations: equations = equations
    """
    equations child of controls.
    """
    limits: limits = limits
    """
    limits child of controls.
    """
    advanced: advanced = advanced
    """
    advanced child of controls.
    """
    command_names = \
        ['reset_solution_controls', 'reset_amg_controls',
         'reset_multi_stage_parameters', 'reset_limits',
         'reset_pseudo_time_method_generic',
         'reset_pseudo_time_method_equations',
         'reset_pseudo_time_method_relaxations',
         'reset_pseudo_time_method_scale_factors']

    reset_solution_controls: reset_solution_controls = reset_solution_controls
    """
    reset_solution_controls command of controls.
    """
    reset_amg_controls: reset_amg_controls = reset_amg_controls
    """
    reset_amg_controls command of controls.
    """
    reset_multi_stage_parameters: reset_multi_stage_parameters = reset_multi_stage_parameters
    """
    reset_multi_stage_parameters command of controls.
    """
    reset_limits: reset_limits = reset_limits
    """
    reset_limits command of controls.
    """
    reset_pseudo_time_method_generic: reset_pseudo_time_method_generic = reset_pseudo_time_method_generic
    """
    reset_pseudo_time_method_generic command of controls.
    """
    reset_pseudo_time_method_equations: reset_pseudo_time_method_equations = reset_pseudo_time_method_equations
    """
    reset_pseudo_time_method_equations command of controls.
    """
    reset_pseudo_time_method_relaxations: reset_pseudo_time_method_relaxations = reset_pseudo_time_method_relaxations
    """
    reset_pseudo_time_method_relaxations command of controls.
    """
    reset_pseudo_time_method_scale_factors: reset_pseudo_time_method_scale_factors = reset_pseudo_time_method_scale_factors
    """
    reset_pseudo_time_method_scale_factors command of controls.
    """
