#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .embedded_face_zone import embedded_face_zone
from .floating_surface_name import floating_surface_name
from .create_floating_disk import create_floating_disk
class disk_id(Group):
    """
    Menu to define the disk face/surface name:
    
     - embedded-face-zone    : select embedded-face-zone name, 
     - floating-surface-name : select floating-surface-name, 
     - create-floating-disk  : create a floating-disk for the current rotor, 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "disk-id"

    child_names = \
        ['embedded_face_zone', 'floating_surface_name']

    embedded_face_zone: embedded_face_zone = embedded_face_zone
    """
    embedded_face_zone child of disk_id.
    """
    floating_surface_name: floating_surface_name = floating_surface_name
    """
    floating_surface_name child of disk_id.
    """
    command_names = \
        ['create_floating_disk']

    create_floating_disk: create_floating_disk = create_floating_disk
    """
    create_floating_disk command of disk_id.
    """
