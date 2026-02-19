import json
import numpy as np
from spikeinterface.core import BaseRecording, Motion
from pynwb import get_class


def from_spikeinterface(recording: BaseRecording, motion: Motion, **kwargs):
    assert isinstance(recording, BaseRecording), f"The input must be a SpikeInterface BaseRecording object, not {type(recording)}."

    recording_tree = [recording]
    while recording_tree[-1].get_parent() is not None:
        recording_tree.append(recording_tree[-1].get_parent())
    has_electrical_series = [hasattr(r, "electrical_series") for r in recording_tree]
    assert any(has_electrical_series), "The recording must have an ElectricalSeries to link the DisplacementSeries to."

    assert isinstance(motion, Motion), f"The input must be a SpikeInterface Motion object, not {type(motion)}."

    recording_nwb = recording_tree[has_electrical_series.index(True)]
    nwbfile = recording_nwb._nwbfile
    
    DisplacementSeries = get_class("DisplacementSeries", "ndx-motion-drift")

    displacement_series = DisplacementSeries(
        name=kwargs.get("name", "DisplacementSeries"),
        description=kwargs.get("description", "DisplacementSeries created from a SpikeInterface Motion object."),
        comments=kwargs.get("comments", json.dumps(dict(interpolation_method=motion.interpolation_method))),
        timestamps=motion.temporal_bins_s[0],
        coordinates=motion.spatial_bins_um,
        data=motion.displacement[0],
        direction=motion.direction,
        unit=kwargs.get("unit", "micrometers"),
        conversion=kwargs.get("conversion", 1.0),
        offset=kwargs.get("offset", 0.0),
        resolution=kwargs.get("resolution", -1.0),
        source_electricalseries=recording_nwb.electrical_series,
        electrodes=nwbfile.create_electrode_table_region(
            description="Electrodes for which the motion drift was estimated.",
            region=np.where(np.isin(nwbfile.electrodes["channel_name"].data[:], recording.channel_ids))[0].tolist()
        ),
    )

    return displacement_series


def to_spikeinterface(displacement_series) -> Motion:
    assert isinstance(displacement_series, get_class("DisplacementSeries", "ndx-motion-drift")), f"The input must be a DisplacementSeries object, not {type(displacement_series)}."
    
    try:
        comments_dict = json.loads(displacement_series.comments)
        interpolation_method = comments_dict["interpolation_method"]
    except:
        interpolation_method = "linear"

    motion = Motion(
        displacement=displacement_series.data[:],
        temporal_bins_s=displacement_series.timestamps[:],
        spatial_bins_um=displacement_series.coordinates[:],
        direction=displacement_series.direction,
        interpolation_method=interpolation_method,
    )
    
    return motion