#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .initialization_type import initialization_type
from .reference_frame_1 import reference_frame
from .defaults import defaults
from .fmg_options import fmg_options
from .localized_turb_init import localized_turb_init
from .hybrid_init_options import hybrid_init_options
from .patch import patch
from .open_channel_auto_init import open_channel_auto_init
from .fmg_initialization import fmg_initialization
from .initialize import initialize
from .compute_defaults import compute_defaults
from .fmg_initialize import fmg_initialize
from .standard_initialize import standard_initialize
from .hybrid_initialize import hybrid_initialize
from .list_defaults import list_defaults
from .init_turb_vel_fluctuations import init_turb_vel_fluctuations
from .init_flow_statistics import init_flow_statistics
from .show_iterations_sampled import show_iterations_sampled
from .show_time_sampled import show_time_sampled
from .dpm_reset import dpm_reset
from .lwf_reset import lwf_reset
from .init_acoustics_options import init_acoustics_options
from .levelset_auto_init import levelset_auto_init
class initialization(Group):
    """
    'initialization' child.
    """

    fluent_name = "initialization"

    child_names = \
        ['initialization_type', 'reference_frame', 'defaults', 'fmg_options',
         'localized_turb_init', 'hybrid_init_options', 'patch',
         'open_channel_auto_init', 'fmg_initialization']

    initialization_type: initialization_type = initialization_type
    """
    initialization_type child of initialization.
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of initialization.
    """
    defaults: defaults = defaults
    """
    defaults child of initialization.
    """
    fmg_options: fmg_options = fmg_options
    """
    fmg_options child of initialization.
    """
    localized_turb_init: localized_turb_init = localized_turb_init
    """
    localized_turb_init child of initialization.
    """
    hybrid_init_options: hybrid_init_options = hybrid_init_options
    """
    hybrid_init_options child of initialization.
    """
    patch: patch = patch
    """
    patch child of initialization.
    """
    open_channel_auto_init: open_channel_auto_init = open_channel_auto_init
    """
    open_channel_auto_init child of initialization.
    """
    fmg_initialization: fmg_initialization = fmg_initialization
    """
    fmg_initialization child of initialization.
    """
    command_names = \
        ['initialize', 'compute_defaults', 'fmg_initialize',
         'standard_initialize', 'hybrid_initialize', 'list_defaults',
         'init_turb_vel_fluctuations', 'init_flow_statistics',
         'show_iterations_sampled', 'show_time_sampled', 'dpm_reset',
         'lwf_reset', 'init_acoustics_options', 'levelset_auto_init']

    initialize: initialize = initialize
    """
    initialize command of initialization.
    """
    compute_defaults: compute_defaults = compute_defaults
    """
    compute_defaults command of initialization.
    """
    fmg_initialize: fmg_initialize = fmg_initialize
    """
    fmg_initialize command of initialization.
    """
    standard_initialize: standard_initialize = standard_initialize
    """
    standard_initialize command of initialization.
    """
    hybrid_initialize: hybrid_initialize = hybrid_initialize
    """
    hybrid_initialize command of initialization.
    """
    list_defaults: list_defaults = list_defaults
    """
    list_defaults command of initialization.
    """
    init_turb_vel_fluctuations: init_turb_vel_fluctuations = init_turb_vel_fluctuations
    """
    init_turb_vel_fluctuations command of initialization.
    """
    init_flow_statistics: init_flow_statistics = init_flow_statistics
    """
    init_flow_statistics command of initialization.
    """
    show_iterations_sampled: show_iterations_sampled = show_iterations_sampled
    """
    show_iterations_sampled command of initialization.
    """
    show_time_sampled: show_time_sampled = show_time_sampled
    """
    show_time_sampled command of initialization.
    """
    dpm_reset: dpm_reset = dpm_reset
    """
    dpm_reset command of initialization.
    """
    lwf_reset: lwf_reset = lwf_reset
    """
    lwf_reset command of initialization.
    """
    init_acoustics_options: init_acoustics_options = init_acoustics_options
    """
    init_acoustics_options command of initialization.
    """
    levelset_auto_init: levelset_auto_init = levelset_auto_init
    """
    levelset_auto_init command of initialization.
    """
