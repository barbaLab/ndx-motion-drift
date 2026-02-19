from importlib.resources import files
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-motion-drift.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not __spec_path.exists():
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-motion-drift.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

DisplacementSeries = get_class("DisplacementSeries", "ndx-motion-drift")
DriftCorrection = get_class("DriftCorrection", "ndx-motion-drift")

__all__ = [
    "DisplacementSeries",
    "DriftCorrection",
]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, __location_of_this_file, __spec_path

# Add custom constructors
from .io import from_spikeinterface, to_spikeinterface

DisplacementSeries.from_spikeinterface = from_spikeinterface
DisplacementSeries.to_spikeinterface = to_spikeinterface
