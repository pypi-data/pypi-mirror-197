#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option import option
from .material import material
from .phase_material import phase_material
class model(Group):
    """
    'model' child.
    """

    fluent_name = "model"

    child_names = \
        ['option', 'material', 'phase_material']

    option: option = option
    """
    option child of model.
    """
    material: material = material
    """
    material child of model.
    """
    phase_material: phase_material = phase_material
    """
    phase_material child of model.
    """
