# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ngio",
#     "marimo",
#     "matplotlib",
#     "scikit-image",
#     "altair",
# ]
# ///

import marimo

__generated_with = "0.23.3"
app = marimo.App(width="full", auto_download=["html"])


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
    - Implement a basic image processing pipeline using ngio: (Maximum Intensity Projection -> Basic segmentation -> Feature extraction)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ngio_classes = mo.mermaid(
        """
        graph TD
            %% === STYLE DEFINITIONS (Easy to modify!) ===
            %% Container nodes - Main containers (BVC navy)
            classDef containerStyle fill:#1B2A4A,stroke:#0D1826,stroke-width:3px,color:#fff,font-weight:bold

            %% Multiscale nodes - Collections of pyramid levels (BVC teal)
            classDef multiscaleStyle fill:#3DBDB8,stroke:#278784,stroke-width:2px,color:#fff,font-weight:bold

            %% Image/Label nodes - Individual pyramid levels (BVC blue)
            classDef imageStyle fill:#4A8FD4,stroke:#2E5C8A,stroke-width:2px,color:#fff

            %% Table nodes - Data tables (BVC green)
            classDef tableStyle fill:#5CB87A,stroke:#3D7A54,stroke-width:2px,color:#fff,font-weight:bold

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
    from ngio.utils import download_ome_zarr_dataset, list_ome_zarr_datasets

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    hcs_path = download_ome_zarr_dataset(
        "CardiomyocyteTiny", download_dir=data_dir
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
def _(data_dir, mo, ome_zarr_container):
    # Step 0: Setup a new "Derived" OME-Zarr container based on the original one
    derived_ome_zarr = ome_zarr_container.derive_image(
        data_dir / "derived.zarr",
        # Let's derive to a 2D image (drop time and z),
        # shape in a derived container can be different from the source but must keep the same
        # number of axes (exeption for channels)
        shape=(
            1,
            1,
            2160,
            5120,
        ),
        # Let's update the channel label
        channels_meta=["DAPI-MIP"],
        # Let's also update to the latest NGFF spec version
        ngff_version="0.5",
        overwrite=True,
    )


    def _compare_containers(orig, deriv):
        attrs = ("levels", "level_paths", "is_3d", "channel_labels")
        # Make last column aligned right for better readability of the "same/changed" marker
        rows = ["| Attribute | Original | Derived |  |", "|---|---|---|---:|"]
        # rows = ["| Attribute | Original | Derived |  |", "|---|---|---|---|"]
        for attr in attrs:
            o, d = getattr(orig, attr), getattr(deriv, attr)
            marker = "✅ same" if o == d else "🔄 changed"
            rows.append(f"| `{attr}` | `{o}` | `{d}` | {marker} |")
        orig_img = orig.get_image()
        deriv_img = deriv.get_image()
        for attr in ("dimensions", "shape", "axes", "dtype"):
            o, d = getattr(orig_img, attr), getattr(deriv_img, attr)
            marker = "✅ same" if o == d else "🔄 changed"
            rows.append(f"| `image.{attr}` | `{o}` | `{d}` | {marker} |")
        return "\n".join(rows)


    metadata_diff = mo.md(
        "**Original vs Derived container**\n\n"
        + _compare_containers(ome_zarr_container, derived_ome_zarr)
    )
    metadata_diff
    return (derived_ome_zarr,)


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


@app.cell
def _(derived_ome_zarr, ome_zarr_container):
    # Step 1: Project the image on the z axis to get a 2D MIP
    image_origin = ome_zarr_container.get_image()
    image_data_lazy = image_origin.get_as_dask()

    # Max intensity projection on the fly with dask, without loading the whole image into RAM
    image_data_lazy_mip = image_data_lazy.max(axis=1)
    image_data_lazy_mip = image_data_lazy_mip[
        :, None, ...
    ]  # add back channel axis

    # Write back the MIP as a new derived image
    derived_image = derived_ome_zarr.get_image()

    derived_image.set_array(image_data_lazy_mip)
    derived_image.consolidate()  # build the pyramid levels
    return (derived_image,)


@app.cell
def _(derived_ome_zarr):
    from ngio import OmeZarrContainer
    import matplotlib.pyplot as plt
    from matplotlib import colors
    from matplotlib.patches import Rectangle
    import numpy as np

    # Stable random colormap with a transparent background entry (label 0 → α=0).
    _rng = np.random.default_rng(42)
    _label_colors = np.zeros((1000, 4))
    _label_colors[:, :3] = _rng.random((1000, 3))
    _label_colors[:, 3] = 0.6
    _label_colors[0] = [0, 0, 0, 0]
    LABEL_CMAP = colors.ListedColormap(_label_colors)


    def plot_image(
        ome_zarr: OmeZarrContainer,
        path: str = "0",
        title: str = "",
        label: str | None = None,
        roi_table: str | None = None,
        **kwargs,
    ):
        image = ome_zarr.get_image(path=path)
        img = image.get_as_numpy(**kwargs)

        plt.figure(figsize=(10, 10))
        plt.imshow(img, cmap="gray")
        plt.title(title)
        plt.axis("off")
        plt.tight_layout()

        if label is not None:
            lbl = ome_zarr.get_label(label, path=path)
            # strip channel selection if present, labels don't have channels
            kwargs = {k: v for k, v in kwargs.items() if k != "channel_selection"}
            lbl_img = lbl.get_as_numpy(**kwargs)
            plt.imshow(lbl_img, cmap=LABEL_CMAP, interpolation="nearest")

        if roi_table is not None:
            # `get_generic_roi_table` accepts both regular RoiTable and
            # MaskingRoiTable — both expose `.rois()` returning Roi objects.
            table = ome_zarr.get_generic_roi_table(roi_table)
            for roi in table.rois():
                # World → pixel using the displayed image's own pixel size,
                # then draw a rectangle from the (start, length) of x/y slices.
                px_roi = roi.to_pixel(pixel_size=image.pixel_size)
                xs, ys = px_roi.get("x"), px_roi.get("y")
                if (
                    xs is None
                    or ys is None
                    or xs.start is None
                    or ys.start is None
                ):
                    continue
                plt.gca().add_patch(
                    Rectangle(
                        (xs.start, ys.start),
                        xs.length,
                        ys.length,
                        fill=False,
                        edgecolor="yellow",
                        linewidth=1.0,
                    )
                )

        plt.show()


    plot_image(
        derived_ome_zarr,
        title="Maximum Intensity Projection (derived image, level 0)",
        axes_order="yx",
    )
    return np, plot_image, plt


@app.cell
def _(derived_image, derived_ome_zarr, np, plot_image):
    # Step 2: Basic segmentation
    from skimage.filters import threshold_otsu
    from skimage.feature import peak_local_max
    from skimage.segmentation import watershed
    from skimage.morphology import remove_small_objects
    from scipy import ndimage as ndi


    def basic_segmentation(image_data):
        # Otsu threshold → distance transform → seeded watershed
        # smooth the input data
        image_data = ndi.gaussian_filter(image_data, sigma=4)
        mask = image_data > threshold_otsu(image_data)
        distance = ndi.distance_transform_edt(mask)
        coords = peak_local_max(distance, min_distance=20, labels=mask)
        markers = np.zeros(distance.shape, dtype=np.int32)
        markers[tuple(coords.T)] = np.arange(1, len(coords) + 1)
        seg = watershed(-distance, markers, mask=mask).astype(np.uint16)
        seg = remove_small_objects(seg, min_size=500)
        return seg


    image_data = derived_image.get_as_numpy(
        channel_selection="DAPI-MIP", axes_order="yx"
    )
    segmentation_mask = basic_segmentation(image_data)

    # Derive a new label and write the segmentation mask back to the OME-Zarr
    derived_label = derived_ome_zarr.derive_label(
        "basic_segmentation", overwrite=True
    )
    derived_label.set_array(segmentation_mask, axes_order="yx")
    derived_label.consolidate()

    plot_image(
        derived_ome_zarr,
        title="Basic Segmentation (derived label, level 0)",
        label="basic_segmentation",
        axes_order="yx",
    )

    roi_table = derived_ome_zarr.build_masking_roi_table(
        label="basic_segmentation"
    )
    derived_ome_zarr.add_table(
        name="basic_segmentation_ROI_table",
        table=roi_table,
        overwrite=True,
    )

    plot_image(
        derived_ome_zarr,
        title="Basic Segmentation (derived label, level 0)",
        roi_table="basic_segmentation_ROI_table",
        axes_order="yx",
    )
    return (derived_label,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.4 Tables

    Tables in ngio are described along **three independent axes** — any combination
    is valid, so you can pick the storage you need without giving up the in-memory
    view or the semantic structure you want.

    - **Backend** *(on-disk storage)*: `AnnData` (default), `CSV`,
      `Parquet`, `JSON`, …your own.
    - **Object** *(in-memory view)*: `AnnData`, `pandas.DataFrame`,
      `polars.LazyFrame`. Every table exposes all three via `.anndata`,
      `.dataframe`, and `.lazy_frame` regardless of the backend.
    - **Type** *(expected layout)*: `FeatureTable`, `RoiTable`, `MaskingRoiTable`,
      `ConditionTable`, …your own.

    The three axes meet at the read/write idiom:

    ```python
    container.add_table(
        name="my_features",
        table=FeatureTable(df, reference_label="basic_segmentation"),
        backend="parquet",          # any backend
        overwrite=True,
    )

    table = container.get_feature_table("my_features")  # type-aware access
    table.dataframe                                     # or .lazy_frame / .anndata
    ```

    Use `container.list_tables()` (optionally with
    `filter_types="masking_roi_table"`, `"feature_table"`, …) to discover what's
    already on a container.
    """)
    return


@app.cell
def _(derived_ome_zarr):
    # Discover what's available on the container
    derived_ome_zarr.list_tables()
    return


@app.cell
def _(derived_image, derived_label, derived_ome_zarr, np):
    # Step 3: Create simple region props table for the segmented objects
    import pandas as pd
    from skimage.measure import regionprops_table
    from ngio.tables import FeatureTable


    def compute_region_props(
        segmentation_mask: np.ndarray, image_data: np.ndarray
    ):
        props = regionprops_table(
            segmentation_mask,
            intensity_image=image_data,
            properties=(
                "label",
                "area",
                "mean_intensity",
                "max_intensity",
                "min_intensity",
                "centroid",
                "eccentricity",
                "solidity",
            ),
        )
        return pd.DataFrame(props)


    segmentation_mask2 = derived_label.get_as_numpy(axes_order="yx")
    image_data2 = derived_image.get_as_numpy(
        channel_selection="DAPI-MIP", axes_order="yx"
    )
    feature_df = compute_region_props(segmentation_mask2, image_data2)

    feature_table = FeatureTable(feature_df, reference_label="basic_segmentation")
    derived_ome_zarr.add_table(
        name="basic_segmentation_features",
        table=feature_table,
        backend="csv",
        overwrite=True,
    )

    feature_table.lazy_frame.collect()  # compute the table (if there are lazy computations)
    return (feature_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3.5 Interactive feature exploration

    Pick any two numeric columns to scatter the per-object features. Switch the
    **selection mode** between a brush (drag a rectangle) and a click (single
    point). Selected objects are previewed on the right with their segmentation
    boundary outlined in red.
    """)
    return


@app.cell
def _(derived_ome_zarr):
    # Let's put it all together
    derived_image_plot = derived_ome_zarr.get_image()
    derived_label_plot = derived_ome_zarr.get_label("basic_segmentation")

    feature_table_plot = derived_ome_zarr.get_feature_table(
        "basic_segmentation_features"
    )
    masking_roi_table_plot = derived_ome_zarr.get_masking_roi_table(
        "basic_segmentation_ROI_table"
    )
    return (
        derived_image_plot,
        derived_label_plot,
        feature_table_plot,
        masking_roi_table_plot,
    )


@app.cell(hide_code=True)
def _(feature_df, mo):
    numeric_cols = list(feature_df.select_dtypes("number").columns)
    x_axis = mo.ui.dropdown(numeric_cols, value="area", label="X axis")
    y_axis = mo.ui.dropdown(numeric_cols, value="mean_intensity", label="Y axis")
    zoom = mo.ui.slider(1.0, 15.0, value=1.0, step=0.1, label="Zoom (preview)")
    mo.hstack([x_axis, y_axis, zoom], justify="start")
    return x_axis, y_axis, zoom


@app.cell(hide_code=True)
def _(feature_table_plot, mo, x_axis, y_axis):
    import altair as alt

    feature_df_alt = feature_table_plot.dataframe

    feature_chart = mo.ui.altair_chart(
        alt.Chart(feature_df_alt)
        .mark_circle(size=80, opacity=0.7)
        .encode(
            x=alt.X(f"{x_axis.value}:Q", title=x_axis.value),
            y=alt.Y(f"{y_axis.value}:Q", title=y_axis.value),
            tooltip=list(feature_df_alt.columns),
        )
        .properties(width=800, height=400)
        .interactive(),
        chart_selection="point",
    )
    return (feature_chart,)


@app.cell(hide_code=True)
def _(
    derived_image_plot,
    derived_label_plot,
    feature_chart,
    masking_roi_table_plot,
    mo,
    plt,
    zoom,
):
    _selection = feature_chart.value
    _selection = (
        _selection.reset_index()
        if _selection is not None and len(_selection)
        else None
    )
    _selected_labels = (
        _selection["label"].tolist()
        if _selection is not None and len(_selection)
        else []
    )

    if len(_selected_labels) == 1:
        _lbl = _selected_labels[0]
        _fig, _ax = plt.subplots(figsize=(6, 6))
        _roi = masking_roi_table_plot.get_label(_lbl).zoom(zoom.value)
        _img = derived_image_plot.get_roi_as_numpy(
            _roi, channel_selection="DAPI-MIP", axes_order="yx"
        )
        _mask = derived_label_plot.get_roi_as_numpy(_roi, axes_order="yx")
        _ax.imshow(_img, cmap="gray")
        _ax.contour(_mask == _lbl, levels=[0.5], colors="red", linewidths=1.5)
        _ax.set_title(f"label {_lbl}")
        _ax.axis("off")
        _fig.tight_layout()
        preview = _fig
    else:
        preview = mo.md(
            "Select a single point to preview the corresponding object segmentation."
        )

    mo.hstack([feature_chart, preview], align="start", widths=[1, 1])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
