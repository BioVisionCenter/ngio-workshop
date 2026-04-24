# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ngio",
#     "marimo",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.23.2"
app = marimo.App(
    width="medium",
    layout_file="data:application/json;base64,ewogICJ0eXBlIjogImdyaWQiLAogICJkYXRhIjogewogICAgImNvbHVtbnMiOiAyNCwKICAgICJyb3dIZWlnaHQiOiAyMCwKICAgICJtYXhXaWR0aCI6IDE0MDAsCiAgICAiYm9yZGVyZWQiOiB0cnVlLAogICAgImNlbGxzIjogWwogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDAsCiAgICAgICAgICA2LAogICAgICAgICAgMgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICAyLAogICAgICAgICAgNiwKICAgICAgICAgIDI3CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogbnVsbAogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgNiwKICAgICAgICAgIDAsCiAgICAgICAgICA2LAogICAgICAgICAgNzAKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBudWxsCiAgICAgIH0KICAgIF0KICB9Cn0=",
    auto_download=["html"],
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction to ngio

    **ngio** is a Python library that provides a clean, object-oriented API for reading, writing, and exploring
    [OME-Zarr](https://ngff.openmicroscopy.org/) files.

    ### Goals of this notebook:
    - Become familiar with ngio, its abstractions, and APIs
    - Open, explore, and process an OME-Zarr.
    - Integrate tabular data (ROIs, feature tables, and more) in your OME-Zarr processing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ngio_classes = mo.mermaid(
        """
        graph TD
            %% === STYLE DEFINITIONS (Easy to modify!) ===
            %% Container nodes - Main containers (purple theme)
            classDef containerStyle fill:#9370DB,stroke:#6A0DAD,stroke-width:3px,color:#fff,font-weight:bold

            %% Multiscale nodes - Collections of pyramid levels (blue theme)
            classDef multiscaleStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff,font-weight:bold

            %% Image/Label nodes - Individual pyramid levels (green theme)
            classDef imageStyle fill:#50C878,stroke:#2D5F3D,stroke-width:2px,color:#fff

            %% Table nodes - Data tables (orange theme)
            classDef tableStyle fill:#FF8C42,stroke:#C65D21,stroke-width:2px,color:#fff,font-weight:bold

            %% === GRAPH STRUCTURE ===
            OZC["OmeZarrContainer"]

            OZC --> IMG["MultiscaleImage"]
            IMG --> IMGL0["Image(path='0')"]
            IMG --> IMGL1["Image(path='1')"]
            IMG --> IMGL2["..."]

            OZC --> LC["LabelsContainer"]
            LC --> OZLC-nuc["nuclei"]
            OZLC-nuc --> OZLC-nucL0["Label(path='0')"]
            OZLC-nuc --> OZLC-nucL1["Label(path='1')"]
            OZLC-nuc --> OZLC-nucL2["..."]
            LC --> OZLC-other["..."]

            OZC --> TBL["TablesContainer"]
            TBL --> TBL-roi["RoiTable"]
            TBL --> TBL-features["FeaturesTable"]
            TBL --> TBL-other["..."]

            %% === APPLY STYLES ===
            class OZC,LC,TBL containerStyle
            class IMG,OZLC-nuc,OZLC-other multiscaleStyle
            class IMGL0,IMGL1,IMGL2,OZLC-nucL0,OZLC-nucL1,OZLC-nucL2 imageStyle
            class TBL-roi,TBL-features,TBL-other tableStyle
        """
    )
    return (ngio_classes,)


@app.cell(hide_code=True)
def _(mo, ngio_classes):
    mo.md(rf"""
    ## 1 Overview

    ### What is the OME-Zarr container?

    The `OME-Zarr Container` in ngio is your entry point to working with OME-Zarr images.

    It provides:

    - **OME-Zarr overview**: get an overview of the OME-Zarr file, including the number of image levels, list of labels, and tables available.
    - **Images**: get access to the images at different resolution levels / pixel sizes.
    - **Label management**: check which labels are available, access them, and create new labels.
    - **Table management**: check which tables are available, access them, and create new tables.
    - **Derive new OME-Zarr images**: create new images based on the original one, with the same or similar metadata.
    - **Edit OME-Zarr Metadata**: high level APIs to modify the OME-Zarr metadata.

    {ngio_classes}

    ### What is the OME-Zarr container not?

    The `OME-Zarr Container` object does not allow the user to interact with the image data directly. For that, we need to use the `Image`, `Label`, and `Table` objects. ngio organises an OME-Zarr file into a small set of composable abstractions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 Setup

    We will use a small sample HCS plate (`CardiomyocyteTinyMip`) that ships with ngio's test datasets.
    The helper `download_ome_zarr_dataset` fetches it into a local temp directory the first time it runs
    (subsequent runs reuse the cached copy).
    We then open a single well image (`B/03/0`) as an `OmeZarrContainer` — this is the object we will
    work with throughout the notebook.
    """)
    return


@app.cell
def _(mo):
    from pathlib import Path
    import ngio
    from ngio.utils import download_ome_zarr_dataset

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    hcs_path = download_ome_zarr_dataset(
        "CardiomyocyteTinyMip", download_dir=data_dir
    )
    image_path = hcs_path / "B" / "03" / "0"
    ome_zarr_container = ngio.open_ome_zarr_container(image_path)
    image = ome_zarr_container.get_image()
    mo.md(f"Opened container: `{image_path}`")
    return data_dir, image, ome_zarr_container


@app.cell(hide_code=True)
def _(mo, ome_zarr_container):
    mo.md(f"""
    ## 3.1 OME-Zarr Overview
    Let's explore the main OME-Zarr Container APIs to explore what's inside our
    OME-Zarr image:
    - Multiscale image metadata:
        - `{ome_zarr_container.levels=}`
        - `{ome_zarr_container.level_paths=}`
        - `{ome_zarr_container.is_3d=}`
        - `{ome_zarr_container.is_time_series=}` 
        - `{ome_zarr_container.channel_labels=}`
    - Labels Container:
        - `{ome_zarr_container.list_labels()=}`
    - Tables Container:
        - `{ome_zarr_container.list_tables()=}`

    ## 3.2 Derive new Images and Labels

    ### Derive a new image container

    `derive_image` creates a **new OME-Zarr container** that clones the pyramid structure,
    pixel sizes, and channel metadata of the source — ready to be filled with processed data.

    ```python
    derived = container.derive_image("output.zarr", overwrite=True)
    ```

    Typical write-back pattern:

    ```python
    out_image = derived.get_image()
    out_image.set_array(processed_data)   # write to level 0
    out_image.consolidate()               # rebuild all other pyramid levels
    ```

    ### Derive a new label

    `derive_label` adds a new **empty label** (segmentation mask) inside an existing container,
    matching the image shape and pyramid structure.

    ```python
    new_label = container.derive_label("my_segmentation", overwrite=True)
    new_label.set_array(mask)
    new_label.consolidate()
    ```
    """)
    return


@app.cell
def _(ome_zarr_container):
    # Many more to explore..
    ome_zarr_container
    return


@app.cell
def _(data_dir, ome_zarr_container):
    # Let's create a new derived empty OME-Zarr container to write results into
    derived = ome_zarr_container.derive_image(
        data_dir / "derived.zarr", overwrite=True
    )

    print(f"Derived container             : {derived}")
    print(f"Level paths                   : {derived.level_paths}")
    print(f"Channel labels                : {derived.channel_labels}")

    # Let's create a new label inside this new container
    derived.derive_label("nuclei_mask")
    print(f"Derived container (with label): {derived}")
    return


@app.cell(hide_code=True)
def _(image, mo):
    mo.md(rf"""
    ## 3.3 Images and Labels

    ### Image

    An `Image` represents **one resolution level** of the multiscale pyramid.
    Get it from the container:

    ```python
    image = container.get_image()                              # highest resolution (default)
    image = container.get_image(path="1")                      # specific pyramid level
    image = container.get_image(pixel_size=ps, strict=False)   # nearest matching resolution
    ```

    Key properties:
    - `{image.dimensions=}`
    - `{image.pixel_size=}`
    - `{image.shape=}`
    - `{image.axes=}`
    - `{image.dtype=}`

    Key methods:
    - **`image.get_as_numpy(...)`** — eager, loads into RAM.
    - **`image.get_as_dask(...)`** — lazy, only reads when computed.
    - **`image.set_array(...)`** — write the data back into the OME-Zarr.
    - **`image.consolidate()`** — consolidate changes to all resolution levels.

    ### Label

    A `Label` stores **integer segmentation masks**
    It has the **same multiscale pyramid** as the image but (in general) no channels
    The API mirrors `Image` exactly.

    ```python
    container.list_labels()                                             # list available labels
    label = container.get_label("nuclei")                               # highest resolution
    label = container.get_label("nuclei", path="1")                     # specific level
    label = container.get_label("nuclei", pixel_size=image.pixel_size)  # matching resolution
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.3 Derive new Images and Labels

    ### Derive a new image container

    `derive_image` creates a **new OME-Zarr container** that clones the pyramid structure,
    pixel sizes, and channel metadata of the source — ready to be filled with processed data.

    ```python
    derived = container.derive_image("output.zarr", overwrite=True)
    ```

    Typical write-back pattern:

    ```python
    out_image = derived.get_image()
    out_image.set_array(processed_data)   # write to level 0
    out_image.consolidate()               # rebuild all other pyramid levels
    ```

    ### Derive a new label

    `derive_label` adds a new **empty label** (segmentation mask) inside an existing container,
    matching the image shape and pyramid structure.

    ```python
    new_label = container.derive_label("my_segmentation", overwrite=True)
    new_label.set_array(mask)
    new_label.consolidate()
    ```
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.4 Tables

    Tables store structured data alongside the image inside the same OME-Zarr container.
    ngio supports three typed tables:

    | Table type | Accessor | Index | Purpose |
    |---|---|---|---|
    | `RoiTable` | `get_roi_table(name)` | string name | Named spatial regions (e.g. fields of view) in world coordinates |
    | `MaskingRoiTable` | `get_masking_roi_table(name)` | integer label ID | Bounding box per segmented object |
    | `FeatureTable` | `get_feature_table(name)` | integer label ID | Per-object measurements as a pandas DataFrame |

    ```python
    container.list_tables()                              # list all tables

    fov   = container.get_roi_table("FOV_ROI_table")      # RoiTable
    nuc   = container.get_masking_roi_table("nuclei_ROI_table")  # MaskingRoiTable
    feats = container.get_feature_table("nuclei")         # FeatureTable
    ```

    A `Roi` from any table can be passed directly to `image.get_roi_as_numpy(roi)` —
    the library converts world coordinates to pixel indices automatically.

    `FeatureTable` exposes its data via `.dataframe` (a pandas DataFrame), one row per object.
    """)
    return


@app.cell
def _(ome_zarr_container):
    fov_table = ome_zarr_container.get_roi_table("FOV_ROI_table")
    nuc_table = ome_zarr_container.get_masking_roi_table("nuclei_ROI_table")
    feat_table = ome_zarr_container.get_feature_table("nuclei")

    print(f"FOV ROIs        : {[r.name for r in fov_table.rois()]}")
    print(f"Nuclei objects  : {len(nuc_table.rois())}")
    print(f"Feature columns : {list(feat_table.dataframe.columns)}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
