import json
import numpy as np
from spikeinterface.core import BaseRecording, Motion
from spikeinterface.extractors.nwbextractors import _retrieve_electrical_series_pynwb
from pynwb import get_class, NWBFile
from pynwb.ecephys import ElectricalSeries


def from_spikeinterface(
        motion: Motion, nwbfile: NWBFile,
        source_electrical_series: ElectricalSeries | str, electrodes,
        **kwargs
    ):
    assert isinstance(motion, Motion), f"The input must be a SpikeInterface Motion object, not {type(motion)}."
    assert isinstance(nwbfile, NWBFile), f"The input must be a PyNWB NWBFile object, not {type(nwbfile)}."
    assert isinstance(source_electrical_series, (ElectricalSeries, str)), f"The source_electrical_series must be either a PyNWB ElectricalSeries object or the path of an ElectricalSeries in the NWBFile, not {type(source_electrical_series)}."

    if isinstance(source_electrical_series, str):
        source_electrical_series = _retrieve_electrical_series_pynwb(nwbfile, source_electrical_series)

    if isinstance(electrodes, (list, np.ndarray)):
        electrodes = nwbfile.create_electrode_table_region(
            description="Electrodes for which the motion drift was estimated.",
            region=np.where(np.isin(nwbfile.electrodes["channel_name"].data[:], electrodes))[0].tolist()
        )

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
        source_electricalseries=source_electrical_series,
        electrodes=electrodes,
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