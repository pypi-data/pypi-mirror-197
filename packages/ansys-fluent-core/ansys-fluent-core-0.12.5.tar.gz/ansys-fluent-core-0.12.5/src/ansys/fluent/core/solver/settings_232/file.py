#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .single_precision_coordinates import single_precision_coordinates
from .binary_legacy_files import binary_legacy_files
from .cff_files import cff_files
from .convert_hanging_nodes_during_read import convert_hanging_nodes_during_read
from .async_optimize import async_optimize
from .write_pdat import write_pdat
from .confirm_overwrite import confirm_overwrite
from .auto_save import auto_save
from .export import export
from .import_ import import_
from .parametric_project import parametric_project
from .cffio_options import cffio_options
from .define_macro import define_macro
from .execute_macro import execute_macro
from .read_macros import read_macros
from .read_1 import read
from .read_case import read_case
from .read_case_data import read_case_data
from .read_case_setting import read_case_setting
from .read_data import read_data
from .read_mesh import read_mesh
from .read_journal import read_journal
from .start_journal import start_journal
from .stop_journal import stop_journal
from .replace_mesh import replace_mesh
from .write import write
from .read_settings import read_settings
from .read_field_functions import read_field_functions
from .read_injections import read_injections
from .read_profile import read_profile
from .read_pdf import read_pdf
from .read_isat_table import read_isat_table
from .show_configuration import show_configuration
from .stop_macro import stop_macro
from .start_transcript import start_transcript
from .stop_transcript import stop_transcript
from .data_file_options import data_file_options
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'convert_hanging_nodes_during_read', 'async_optimize', 'write_pdat',
         'confirm_overwrite', 'auto_save', 'export', 'import_',
         'parametric_project', 'cffio_options']

    single_precision_coordinates: single_precision_coordinates = single_precision_coordinates
    """
    single_precision_coordinates child of file.
    """
    binary_legacy_files: binary_legacy_files = binary_legacy_files
    """
    binary_legacy_files child of file.
    """
    cff_files: cff_files = cff_files
    """
    cff_files child of file.
    """
    convert_hanging_nodes_during_read: convert_hanging_nodes_during_read = convert_hanging_nodes_during_read
    """
    convert_hanging_nodes_during_read child of file.
    """
    async_optimize: async_optimize = async_optimize
    """
    async_optimize child of file.
    """
    write_pdat: write_pdat = write_pdat
    """
    write_pdat child of file.
    """
    confirm_overwrite: confirm_overwrite = confirm_overwrite
    """
    confirm_overwrite child of file.
    """
    auto_save: auto_save = auto_save
    """
    auto_save child of file.
    """
    export: export = export
    """
    export child of file.
    """
    import_: import_ = import_
    """
    import_ child of file.
    """
    parametric_project: parametric_project = parametric_project
    """
    parametric_project child of file.
    """
    cffio_options: cffio_options = cffio_options
    """
    cffio_options child of file.
    """
    command_names = \
        ['define_macro', 'execute_macro', 'read_macros', 'read', 'read_case',
         'read_case_data', 'read_case_setting', 'read_data', 'read_mesh',
         'read_journal', 'start_journal', 'stop_journal', 'replace_mesh',
         'write', 'read_settings', 'read_field_functions', 'read_injections',
         'read_profile', 'read_pdf', 'read_isat_table', 'show_configuration',
         'stop_macro', 'start_transcript', 'stop_transcript',
         'data_file_options']

    define_macro: define_macro = define_macro
    """
    define_macro command of file.
    """
    execute_macro: execute_macro = execute_macro
    """
    execute_macro command of file.
    """
    read_macros: read_macros = read_macros
    """
    read_macros command of file.
    """
    read: read = read
    """
    read command of file.
    """
    read_case: read_case = read_case
    """
    read_case command of file.
    """
    read_case_data: read_case_data = read_case_data
    """
    read_case_data command of file.
    """
    read_case_setting: read_case_setting = read_case_setting
    """
    read_case_setting command of file.
    """
    read_data: read_data = read_data
    """
    read_data command of file.
    """
    read_mesh: read_mesh = read_mesh
    """
    read_mesh command of file.
    """
    read_journal: read_journal = read_journal
    """
    read_journal command of file.
    """
    start_journal: start_journal = start_journal
    """
    start_journal command of file.
    """
    stop_journal: stop_journal = stop_journal
    """
    stop_journal command of file.
    """
    replace_mesh: replace_mesh = replace_mesh
    """
    replace_mesh command of file.
    """
    write: write = write
    """
    write command of file.
    """
    read_settings: read_settings = read_settings
    """
    read_settings command of file.
    """
    read_field_functions: read_field_functions = read_field_functions
    """
    read_field_functions command of file.
    """
    read_injections: read_injections = read_injections
    """
    read_injections command of file.
    """
    read_profile: read_profile = read_profile
    """
    read_profile command of file.
    """
    read_pdf: read_pdf = read_pdf
    """
    read_pdf command of file.
    """
    read_isat_table: read_isat_table = read_isat_table
    """
    read_isat_table command of file.
    """
    show_configuration: show_configuration = show_configuration
    """
    show_configuration command of file.
    """
    stop_macro: stop_macro = stop_macro
    """
    stop_macro command of file.
    """
    start_transcript: start_transcript = start_transcript
    """
    start_transcript command of file.
    """
    stop_transcript: stop_transcript = stop_transcript
    """
    stop_transcript command of file.
    """
    data_file_options: data_file_options = data_file_options
    """
    data_file_options command of file.
    """
