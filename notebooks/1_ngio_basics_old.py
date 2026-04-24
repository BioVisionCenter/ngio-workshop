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
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
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
            LC --> OZLC-cell["..."]

            OZC --> TBL["TablesContainer"]
            TBL --> TBL-roi["RoiTable"]
            TBL --> TBL-features["FeaturesTable"]

            %% === APPLY STYLES ===
            class OZC,LC,TBL containerStyle
            class IMG,OZLC-nuc,OZLC-cell multiscaleStyle
            class IMGL0,IMGL1,IMGL2,OZLC-nucL0,OZLC-nucL1,OZLC-nucL2 imageStyle
            class TBL-roi,TBL-features tableStyle
        """
    )
    return (ngio_classes,)


@app.cell(hide_code=True)
def _(mo, ngio_classes):
    mo.md(rf"""
    # Introduction to ngio

    TODO what is ngio?

    ## Overview
    {ngio_classes}

    TODO
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    from pathlib import Path
    import shutil
    import tempfile

    import numpy as np
    import matplotlib.pyplot as plt

    import ngio
    from ngio import (
        Roi,
        PixelSize,
        create_empty_ome_zarr,
        create_ome_zarr_from_array,
        open_ome_zarr_container,
    )
    from ngio.tables import FeatureTable, MaskingRoiTable, RoiTable
    from ngio.utils import download_ome_zarr_dataset

    return (
        Path,
        Roi,
        RoiTable,
        create_empty_ome_zarr,
        create_ome_zarr_from_array,
        download_ome_zarr_dataset,
        np,
        open_ome_zarr_container,
        plt,
        shutil,
        tempfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup — Sample Data

    ngio ships a small helper to download built-in datasets.
    Here we use `CardiomyocyteTinyMip`, a maximum-intensity-projection (MIP) of a cardiomyocyte
    differentiation experiment.  The download is cached after the first run.

    The dataset is an HCS (High-Content Screening) plate stored in OME-Zarr.
    We will work with well **B03**, image path **0**.
    """)
    return


@app.cell
def _(Path, download_ome_zarr_dataset):
    dataset_path = download_ome_zarr_dataset(
        "CardiomyocyteTinyMip",
        download_dir=Path("./data"),
    )
    print(f"Dataset path: {dataset_path}")
    return


@app.cell(hide_code=True)
def _(mo, ngio_classes):
    mo.md(rf"""
    ## 1. Overview
    {ngio_classes}

    TODO add a
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ## 1. OmeZarrContainer

    `OmeZarrContainer` is the **entry point** for a single OME-Zarr image.
    Open one with `open_ome_zarr_container(path)`.

    It gives you:
    - An overview of the multiscale **pyramid** (number of levels, paths)
    - Access to **images** at different resolutions
    - Access to **labels** (segmentation masks)
    - Access to **tables** (ROIs, features, …)

    > What it does *not* do: direct array access.  For that you need an `Image`, `Label`, or `Table` object.

    ```mermaid
    graph TD
        OZC["OmeZarrContainer"]

        OZC --> IMG["Images (pyramid levels)"]
        OZC --> LBL["Labels"]
        OZC --> TBL["Tables"]

        IMG --> IMG0["Image — level 0 (full res)"]
        IMG --> IMG1["Image — level 1 (½ res)"]
        IMG --> IMGN["Image — level N (…)"]

        LBL --> LBL1["Label (e.g. nuclei)"]
        LBL1 --> LBLP0["Label level 0"]
        LBL1 --> LBLPN["Label level N (…)"]

        TBL --> ROI["RoiTable"]
        TBL --> MROI["MaskingRoiTable"]
        TBL --> FEAT["FeatureTable"]

        MROI -->|"references"| LBL1
    ```
    """)
    return


@app.cell
def _(ome_zarr):
    derived_ome_zarr = ome_zarr.derive_image(store="./tmp_data/derived.zarr", overwrite=True, copy_labels=True, copy_tables=True)

    image = ome_zarr.get_image()
    derived_image = derived_ome_zarr.get_image()
    derived_image.set_array(image.get_as_dask())
    return derived_ome_zarr, image


@app.cell
def _(derived_ome_zarr):
    derived_ome_zarr.list_tables()
    return


@app.cell
def _(open_ome_zarr_container):
    #ome_zarr = open_ome_zarr_container("https://raw.githubusercontent.com/"
    #    "fractal-analytics-platform/fractal-ome-zarr-examples/"
    #    "refs/heads/main/v04/"
    #    "20200812-CardiomyocyteDifferentiation14-Cycle1_B_03_mip.zarr/"
    #)
    ome_zarr = open_ome_zarr_container("data/20200812-CardiomyocyteDifferentiation14-Cycle1-tiny-mip.zarr/B/03/0")
    print(ome_zarr)
    print()
    print(f"Pyramid levels : {ome_zarr.levels}")
    print(f"Level paths    : {ome_zarr.level_paths}")
    print(f"Is 3D          : {ome_zarr.is_3d}")
    print(f"Is time series : {ome_zarr.is_time_series}")
    print(f"Channel labels : {ome_zarr.channel_labels}")
    print(f"Labels         : {ome_zarr.list_labels()}")
    print(f"Tables         : {ome_zarr.list_tables()}")
    return (ome_zarr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Editing Metadata

    ngio can update the image metadata in-place.  Common operations:

    | Method | Effect |
    |---|---|
    | `set_channel_labels(names)` | Rename channels |
    | `set_channel_colors(hex_list)` | Set display colours (hex strings) |
    | `set_channel_windows_with_percentiles(p)` | Auto-compute display min/max |
    | `set_axes_units(space_unit=…)` | Set physical units |
    | `set_name(name)` | Name the image in the metadata |

    These changes are written directly to the Zarr store's `.zattrs`.
    """)
    return


@app.cell
def _(ome_zarr):
    print("Before:", ome_zarr.channel_labels)
    ome_zarr.set_channel_labels(["DAPI"])
    ome_zarr.set_channel_colors(["0000FF"])
    ome_zarr.set_channel_windows_with_percentiles(percentiles=(0.5, 99.5))
    ome_zarr.set_axes_units(space_unit="micrometer")
    print("After :", ome_zarr.channel_labels)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Image

    `Image` represents **one resolution level** of the pyramid.
    Get it from the container with `get_image()`:

    ```python
    image = ome_zarr.get_image()              # highest resolution (default)
    image = ome_zarr.get_image(path="1")      # specific pyramid level by path
    image = ome_zarr.get_image(pixel_size=ps) # exact pixel size
    image = ome_zarr.get_image(pixel_size=ps, strict=False)  # nearest resolution
    ```

    An `Image` exposes rich metadata and read/write methods, but does not load
    any array data until you explicitly ask for it.
    """)
    return


@app.cell
def _(ome_zarr):
    image = ome_zarr.get_image()
    print(image)
    print()
    print(f"Shape          : {image.shape}")
    print(f"Dtype          : {image.dtype}")
    print(f"Chunks         : {image.chunks}")
    print(f"Axes           : {image.axes}")
    print(f"Pixel size     : {image.pixel_size}")
    print(f"Dimensions     : {image.dimensions}")
    print(f"Channel labels : {image.channel_labels}")
    return (image,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Resolution Pyramid

    Each successive pyramid level is spatially downsampled (typically by 2×).
    Lower levels are faster to read and useful for overview visualisations.
    """)
    return


@app.cell
def _(ome_zarr):
    for _path in ome_zarr.level_paths:
        _img = ome_zarr.get_image(path=_path)
        _ps = _img.pixel_size
        print(f"Level {_path}:  shape={_img.shape}  pixel_size={_ps.x:.4f} µm")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading Image Data

    Two loading modes:

    - **`get_as_numpy()`** — eager: loads everything into RAM.  Good for small arrays.
    - **`get_as_dask()`** — lazy: returns a Dask array; data is read only when computed.
      Prefer this for large images.

    Both accept keyword arguments for **channel selection** and **axis slicing**:

    ```python
    image.get_as_numpy(channel_selection="DAPI")           # select by name
    image.get_as_numpy(channel_selection="DAPI",
                       x=slice(0, 256), y=slice(0, 256))   # spatial crop
    image.get_as_numpy(axes_order=["z", "y", "x", "c"])    # reorder output axes
    ```
    """)
    return


@app.cell
def _(image, np):
    array = image.get_as_numpy()
    print(f"Full array  shape={array.shape}  dtype={array.dtype}")

    dapi_array = image.get_as_numpy(channel_selection="DAPI")
    print(f"DAPI channel shape={dapi_array.shape}")

    dask_arr = image.get_as_dask()
    print(f"Dask array  {dask_arr}")

    print(f"\nMemory (full array): {array.nbytes / 1e6:.1f} MB")
    print(f"Value range: [{np.percentile(array, 0.5):.0f}, {np.percentile(array, 99.5):.0f}]")
    return (array,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visualising the Image
    """)
    return


@app.cell
def _(np, ome_zarr, plt):
    _img_vis = ome_zarr.get_image(path="2")
    _frame = _img_vis.get_as_numpy()[0, 0]  # (c, z, y, x) → take c=0, z=0

    _vmin, _vmax = np.percentile(_frame, [0.5, 99.5])
    _ps = _img_vis.pixel_size.x

    _fig, _ax = plt.subplots(figsize=(10, 4))
    _ax.imshow(_frame, cmap="gray", vmin=_vmin, vmax=_vmax)
    _ax.set_title(f"DAPI — pyramid level 2  ({_ps:.4f} µm/px)")
    _ax.axis("off")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Writing Image Data

    Use `set_array()` to write data back to a single resolution level, then
    call `consolidate()` to rebuild the entire pyramid by downsampling.

    ```python
    image.set_array(data)       # write to level 0
    image.consolidate()          # propagate to all other levels
    ```

    A common pattern is to **derive** a new image from an existing container —
    this copies the metadata (shape, pixel sizes, channel names) into a fresh
    Zarr store, ready to be filled with processed data:

    ```python
    derived = ome_zarr.derive_image("output.zarr", overwrite=True)
    out_img  = derived.get_image()
    out_img.set_array(processed_data)
    out_img.consolidate()
    ```
    """)
    return


@app.cell
def _(array, np, ome_zarr, shutil, tempfile):
    _tmp = tempfile.mkdtemp()
    try:
        _derived = ome_zarr.derive_image(_tmp + "/derived.zarr", overwrite=True)
        _out = _derived.get_image()
        _inverted = np.iinfo(array.dtype).max - array  # simple inversion
        _out.set_array(_inverted)
        _out.consolidate()
        print(f"Derived container: {_derived}")
        print(f"Level paths      : {_derived.level_paths}")
    finally:
        shutil.rmtree(_tmp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Label

    `Label` stores **integer segmentation masks** alongside the image in the same
    OME-Zarr container, under a `labels/` sub-group.

    - Each pixel holds an **integer ID**: 0 = background, 1… N = object IDs.
    - Labels have the **same multiscale pyramid** structure as the parent image.
    - Shape is `(z, y, x)` — **no channel axis**.
    - API is identical to `Image` (same `get_as_numpy`, `set_array`, etc.).

    ```python
    ome_zarr.list_labels()            # list available labels
    label = ome_zarr.get_label("nuclei")           # highest resolution
    label = ome_zarr.get_label("nuclei", path="1") # specific level
    label = ome_zarr.get_label("nuclei",
                               pixel_size=ps, strict=False)  # nearest resolution
    ```
    """)
    return


@app.cell
def _(np, ome_zarr):
    print("Available labels:", ome_zarr.list_labels())

    label = ome_zarr.get_label("nuclei")
    print(f"\n{label}")
    print(f"Shape  : {label.shape}")
    print(f"Dtype  : {label.dtype}")

    _lbl_array = label.get_as_numpy()
    _ids = np.unique(_lbl_array)
    print(f"Unique IDs (first 10): {_ids[:10]}")
    print(f"Number of objects    : {len(_ids) - 1}")  # exclude 0 (background)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Image + Label Overlay
    """)
    return


@app.cell
def _(np, ome_zarr):
    _img_vis = ome_zarr.get_image(path="2")
    _lbl_vis = ome_zarr.get_label("nuclei", pixel_size=_img_vis.pixel_size, strict=False)
    frame_img = _img_vis.get_as_numpy()[0, 0]
    frame_lbl = _lbl_vis.get_as_numpy()[0]
    _vmin, _vmax = np.percentile(frame_img, [0.5, 99.5])
    vmin, vmax = float(_vmin), float(_vmax)
    return frame_img, frame_lbl, vmax, vmin


@app.cell
def _(mo):
    alpha_slider = mo.ui.slider(
        start=0.0, stop=1.0, step=0.05, value=0.4, label="Overlay alpha"
    )
    show_overlay = mo.ui.switch(value=True, label="Show overlay")
    cmap_dropdown = mo.ui.dropdown(
        options=["Reds", "Blues", "Greens", "hot"],
        value="Reds",
        label="Overlay colormap",
    )
    mo.vstack([
        mo.md("**Adjust visualization parameters:**"),
        mo.hstack([alpha_slider, show_overlay, cmap_dropdown], justify="start"),
    ])
    return alpha_slider, cmap_dropdown, show_overlay


@app.cell
def _(
    alpha_slider,
    cmap_dropdown,
    frame_img,
    frame_lbl,
    plt,
    show_overlay,
    vmax,
    vmin,
):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _axes[0].imshow(frame_img, cmap="gray", vmin=vmin, vmax=vmax)
    _axes[0].set_title("DAPI")
    _axes[0].axis("off")

    _axes[1].imshow(frame_img, cmap="gray", vmin=vmin, vmax=vmax)
    if show_overlay.value:
        _axes[1].imshow(
            frame_lbl > 0,
            cmap=cmap_dropdown.value,
            alpha=alpha_slider.value,
            interpolation="none",
        )
        _axes[1].set_title(f"DAPI + nuclei mask (α={alpha_slider.value:.2f})")
    else:
        _axes[1].set_title("DAPI (overlay hidden)")
    _axes[1].axis("off")

    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Deriving a New Label

    `derive_label(name)` creates a new **empty** label in the container with
    the same shape and pyramid structure as the image — ready to be filled
    with a segmentation result.

    ```python
    new_label = ome_zarr.derive_label("my_segmentation", overwrite=True)
    new_label.set_array(segmentation_mask)
    new_label.consolidate()
    ```
    """)
    return


@app.cell
def _(ome_zarr, shutil, tempfile):
    _tmp = tempfile.mkdtemp()
    try:
        _derived = ome_zarr.derive_image(_tmp + "/derived_labels.zarr", overwrite=True)
        _new_lbl = _derived.derive_label("my_label", overwrite=True)
        print(f"New label  : {_new_lbl}")
        print(f"Shape      : {_new_lbl.shape}")
        print(f"Dtype      : {_new_lbl.dtype}")
        print(f"Level paths: {[_new_lbl.path]}")
    finally:
        shutil.rmtree(_tmp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Tables

    Tables are **not** part of the core OME-Zarr spec but are supported by ngio
    following the [Fractal table specification](https://fractal-analytics-platform.github.io/fractal-tasks-core/tables/).
    They are backed by [AnnData](https://anndata.readthedocs.io/) and stored inside the Zarr container.

    ngio supports three typed tables:

    | Table type | Purpose | Index |
    |---|---|---|
    | `RoiTable` | Arbitrary spatial regions (e.g. fields of view) | string name |
    | `MaskingRoiTable` | Bounding box per segmented object | integer label ID |
    | `FeatureTable` | Per-object measurements | integer label ID |

    ```python
    ome_zarr.list_tables()                           # list all tables
    ome_zarr.get_roi_table("FOV_ROI_table")          # typed accessor
    ome_zarr.get_masking_roi_table("nuclei_ROI_table")
    ome_zarr.get_feature_table("nuclei")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4a. RoiTable — Field-of-View Regions

    `RoiTable` stores named `Roi` objects in **world coordinates** (µm).
    The `FOV_ROI_table` contains the microscope fields of view.
    """)
    return


@app.cell
def _(ome_zarr):
    fov_table = ome_zarr.get_roi_table("FOV_ROI_table")
    print(fov_table)
    print()
    print("ROI names:", [r.name for r in fov_table.rois()])

    fov_roi = fov_table.rois()[0]
    print(f"\nFirst ROI: {fov_roi}")
    return (fov_roi,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A `Roi` can be passed directly to `image.get_roi_as_numpy(roi)` to read the
    corresponding spatial patch.  The library converts world coordinates → pixel
    indices automatically.
    """)
    return


@app.cell
def _(fov_roi, image, np, plt):
    fov_array = image.get_roi_as_numpy(fov_roi, channel_selection="DAPI")
    print(f"FOV patch shape: {fov_array.shape}")

    _frame = fov_array[0]  # (z, y, x) after channel_selection squeeze → take z=0
    _vmin, _vmax = np.percentile(_frame, [0.5, 99.5])

    _fig, _ax = plt.subplots(figsize=(6, 5))
    _ax.imshow(_frame, cmap="gray", vmin=_vmin, vmax=_vmax)
    _ax.set_title(f"ROI: {fov_roi.name}")
    _ax.axis("off")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4b. MaskingRoiTable — Per-Object Bounding Boxes

    `MaskingRoiTable` stores one **bounding-box ROI per segmented object**, indexed
    by integer label ID.  It links directly to a `Label`.

    Use `get_label(id)` to retrieve the ROI for a specific object.
    """)
    return


@app.cell
def _(ome_zarr):
    nuc_roi_table = ome_zarr.get_masking_roi_table("nuclei_ROI_table")
    print(nuc_roi_table)
    print(f"Reference label: {nuc_roi_table.reference_label}")
    print(f"Number of ROIs : {len(nuc_roi_table.rois())}")

    _first_id = nuc_roi_table.rois()[0].label
    _roi = nuc_roi_table.get_label(_first_id)
    print(f"\nROI for object {_first_id}: {_roi}")
    return (nuc_roi_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4c. FeatureTable — Per-Object Measurements

    `FeatureTable` holds arbitrary measurements indexed by integer label ID —
    one row per segmented object.  Access the underlying pandas DataFrame via `.dataframe`.
    """)
    return


@app.cell
def _(ome_zarr):
    feature_table = ome_zarr.get_feature_table("nuclei")
    print(feature_table)
    print()
    feature_table.dataframe.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4d. Building Tables Programmatically

    Tables can be created in memory and then persisted with `add_table()`:

    ```python
    # Whole-image ROI (convenience builder)
    roi_table = ome_zarr.build_image_roi_table("whole_image")

    # Per-object bounding boxes from a label (convenience builder)
    masking_table = ome_zarr.build_masking_roi_table("nuclei")

    # Manual ROI creation
    roi = Roi.from_values(
        name="patch",
        slices={"x": (0.0, 50.0), "y": (0.0, 50.0)},  # µm
        space="world",
    )
    table = RoiTable(rois=[roi])

    # Save to disk
    ome_zarr.add_table("my_roi_table", table, overwrite=True)
    ```
    """)
    return


@app.cell
def _(Roi, RoiTable, ome_zarr):
    _whole_img_table = ome_zarr.build_image_roi_table("whole_image")
    print("Whole-image ROI table:", _whole_img_table)

    _masking_table = ome_zarr.build_masking_roi_table("nuclei")
    print("Masking ROI table    :", _masking_table)

    custom_roi = Roi.from_values(
        name="custom_patch",
        slices={"x": (0.0, 50.0), "y": (0.0, 50.0)},
        space="world",
    )
    _custom_table = RoiTable(rois=[custom_roi])
    print(f"\nCustom ROI: {custom_roi}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. MaskedImage

    `MaskedImage` combines an `Image` with a `MaskingRoiTable` so you can
    retrieve data **for individual segmented objects** without iterating manually.

    | Method | Returns |
    |---|---|
    | `get_roi_as_numpy(label=N)` | Bounding-box crop around object N |
    | `get_roi_masked(label=N)` | Same crop, pixels outside mask zeroed |
    | `zoom_factor` argument | Pad the crop by this factor for context |

    ```python
    masked_image = ome_zarr.get_masked_image("nuclei")
    crop   = masked_image.get_roi_as_numpy(label=42, channel_selection="DAPI", zoom_factor=1.5)
    masked = masked_image.get_roi_masked(label=42, channel_selection="DAPI", zoom_factor=1.5)
    ```
    """)
    return


@app.cell
def _(ome_zarr):
    masked_image = ome_zarr.get_masked_image("nuclei")
    print(masked_image)
    return (masked_image,)


@app.cell
def _(mo, nuc_roi_table):
    _label_ids = sorted(
        [r.label for r in nuc_roi_table.rois() if r.label is not None]
    )
    nucleus_ids = _label_ids

    slider = mo.ui.slider(
        start=0,
        stop=len(nucleus_ids) - 1,
        step=1,
        label=f"Nucleus index  (0 – {len(nucleus_ids) - 1})",
        value=0,
    )
    mo.vstack([
        mo.md(f"**{len(nucleus_ids)} nuclei** detected.  Use the slider to browse individual objects."),
        slider,
    ])
    return nucleus_ids, slider


@app.cell
def _(masked_image, np, nucleus_ids, plt, slider):
    _nid = nucleus_ids[slider.value]

    _crop_raw    = masked_image.get_roi_as_numpy(label=_nid, channel_selection="DAPI", zoom_factor=1.5)
    _crop_masked = masked_image.get_roi_masked(label=_nid, channel_selection="DAPI", zoom_factor=1.5)

    _frame_r = _crop_raw[0]    # (z, y, x) after channel_selection squeeze → take z=0
    _frame_m = _crop_masked[0]
    _vmin = float(np.percentile(_frame_r[_frame_r > 0], 1)) if _frame_r.max() > 0 else 0
    _vmax = float(np.percentile(_frame_r[_frame_r > 0], 99)) if _frame_r.max() > 0 else 1

    _fig, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _axes[0].imshow(_frame_r, cmap="gray", vmin=_vmin, vmax=_vmax)
    _axes[0].set_title(f"Nucleus {_nid} — bounding box (zoom ×1.5)")
    _axes[0].axis("off")

    _axes[1].imshow(_frame_m, cmap="gray", vmin=_vmin, vmax=_vmax)
    _axes[1].set_title(f"Nucleus {_nid} — pixels outside mask zeroed")
    _axes[1].axis("off")

    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Creating OME-Zarr Images

    Three patterns for writing new OME-Zarr containers:

    | Function | Use when |
    |---|---|
    | `create_ome_zarr_from_array(store, array, …)` | You already have a NumPy array |
    | `create_empty_ome_zarr(store, shape, …)` | You want to pre-allocate then fill |
    | `container.derive_image(store, …)` | You want the same metadata as an existing image |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6a. From a NumPy array
    """)
    return


@app.cell
def _(create_ome_zarr_from_array, np, shutil, tempfile):
    _tmp = tempfile.mkdtemp()
    try:
        _data = np.random.randint(0, 1000, (1, 1, 256, 256), dtype=np.uint16)
        _container = create_ome_zarr_from_array(
            store=_tmp + "/from_array.zarr",
            array=_data,
            pixelsize=0.1625,
            channels_meta=["DAPI"],
            overwrite=True,
        )
        print(_container)
        print("Level paths:", _container.level_paths)
        print("Shape level 0:", _container.get_image().shape)
    finally:
        shutil.rmtree(_tmp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6b. Empty container
    """)
    return


@app.cell
def _(create_empty_ome_zarr, np, shutil, tempfile):
    _tmp = tempfile.mkdtemp()
    try:
        _container = create_empty_ome_zarr(
            store=_tmp + "/empty.zarr",
            shape=(1, 1, 512, 512),
            pixelsize=0.325,
            channels_meta=["GFP"],
            dtype="float32",
            overwrite=True,
        )
        _img = _container.get_image()
        _img.set_array(np.zeros(_img.shape, dtype="float32"))
        _img.consolidate()
        print(_container)
        print("Written shape:", _container.get_image().shape)
    finally:
        shutil.rmtree(_tmp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6c. Derive from existing container
    """)
    return


@app.cell
def _(ome_zarr, shutil, tempfile):
    _tmp = tempfile.mkdtemp()
    try:
        _derived = ome_zarr.derive_image(_tmp + "/derived.zarr", overwrite=True)
        print(_derived)
        print("Level paths     :", _derived.level_paths)
        print("Channel labels  :", _derived.channel_labels)
        print("Pixel size      :", _derived.get_image().pixel_size)
    finally:
        shutil.rmtree(_tmp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    | Abstraction | How to get it | Primary use |
    |---|---|---|
    | `OmeZarrContainer` | `open_ome_zarr_container(path)` | Inspect the store; access images, labels, tables |
    | `Image` | `container.get_image()` | Read / write array data at a given resolution |
    | `Label` | `container.get_label(name)` | Read / write integer segmentation masks |
    | `RoiTable` | `container.get_roi_table(name)` | Named spatial regions in world coordinates |
    | `MaskingRoiTable` | `container.get_masking_roi_table(name)` | Per-object bounding boxes indexed by label ID |
    | `FeatureTable` | `container.get_feature_table(name)` | Per-object measurements as a pandas DataFrame |
    | `MaskedImage` | `container.get_masked_image(label_name)` | Per-object crops with optional mask application |
    | Creation | `create_ome_zarr_from_array`, `create_empty_ome_zarr`, `derive_image` | Write new OME-Zarr stores |

    **Next steps:**

    - [ngio documentation](https://fractal-analytics-platform.github.io/ngio/)
    - [ngio GitHub](https://github.com/fractal-analytics-platform/ngio)
    - Explore the other notebooks in this workshop for image processing, segmentation, and HCS workflows.
    """)
    return


if __name__ == "__main__":
    app.run()
