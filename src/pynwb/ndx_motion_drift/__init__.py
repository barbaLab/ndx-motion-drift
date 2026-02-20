from importlib.resources import files
from pynwb import load_namespaces, get_class, register_class
from pynwb.core import MultiContainerInterface

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-motion-drift.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not __spec_path.exists():
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-motion-drift.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

DisplacementSeries = get_class("DisplacementSeries", "ndx-motion-drift")
@register_class("MotionDrift", "ndx-motion-drift")
class MotionDrift(MultiContainerInterface):
    """
    Displacement data from one or more channels. This can be used to store the output of motion drift estimation and correction algorithms.
    """

    __clsconf__ = [{
        'attr': 'displacement_series',
        'type': DisplacementSeries,
        'add': 'add_displacement_series',
        'get': 'get_displacement_series',
        'create': 'create_displacement_series',
    }]

__all__ = [
    "DisplacementSeries",
    "MotionDrift",
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, __location_of_this_file, __spec_path

# Add custom constructors
from .io import from_spikeinterface, to_spikeinterface

DisplacementSeries.from_spikeinterface = from_spikeinterface
DisplacementSeries.to_spikeinterface = to_spikeinterface
