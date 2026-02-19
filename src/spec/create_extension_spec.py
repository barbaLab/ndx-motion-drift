# -*- coding: utf-8 -*-
from pathlib import Path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

from pynwb.spec import NWBDatasetSpec, NWBLinkSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-motion-drift""",
        version="""0.1.0""",
        doc="""This extension provides neurodata types for motion drift estimation in ecephys.""",
        author=[
            "Francesco Negri",
        ],
        contact=[
            "francesco.negri@edu.unige.it",
        ],
    )
    ns_builder.include_namespace("core")

    displacement_series = NWBGroupSpec(
        neurodata_type_def="DisplacementSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include motion drift displacements along time at multiple depths.",
        attributes=[
            NWBAttributeSpec(
                name="direction",
                doc="The displacement direction (e.g., 'y').",
                dtype="text"
            ),
            NWBAttributeSpec(
                name="unit",
                doc="The unit of the displacements.",
                dtype="text",
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="The displacements along the specified direction (in micrometers).",
                dims=("num_temporal_bins", "num_spatial_bins"),
                shape=(None, None),
            ),
            NWBDatasetSpec(
                name="timestamps",
                doc="The timestamps at which the displacements are measured (in seconds).",
                dims=("num_temporal_bins",),
                shape=(None,),
                value="seconds",
            ),
            NWBDatasetSpec(
                name="coordinates",
                doc="The coordinates along the specified direction at which the displacements are measured (in micrometers).",
                dims=("num_spatial_bins",),
                shape=(None,),
            ),
            NWBDatasetSpec(
                name="electrodes",
                neurodata_type_inc="DynamicTableRegion",
                doc="DynamicTableRegion pointer to the electrodes that this time series was generated from.",
            )
        ],
        links=[
            NWBLinkSpec(
                name="source_electricalseries",
                doc="Link to the ElectricalSeries that is the source of the motion drift estimation.",
                target_type="ElectricalSeries",
            ),
        ],
    )

    drift_correction = NWBGroupSpec(
        neurodata_type_def="DriftCorrection",
        neurodata_type_inc="NWBDataInterface",
        doc="Displacement data from one or more channels. This can be used to store the output of motion drift estimation and correction algorithms.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="DisplacementSeries",
                doc="DisplacementSeries object(s) containing the motion drift estimation results.",
                quantity="+",
            ),
        ]
    )

    new_data_types = [displacement_series, drift_correction]

    # export the spec to yaml files in the root spec folder
    output_dir = str((Path(__file__).parent.parent.parent / "spec").absolute())
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
