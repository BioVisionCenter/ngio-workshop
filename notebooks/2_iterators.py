# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ngio",
#     "marimo",
#     "matplotlib",
#     "scikit-image",
# ]
# ///

import marimo

__generated_with = "0.23.2"
app = marimo.App(
    width="columns",
    layout_file="data:application/json;base64,ewogICJ0eXBlIjogImdyaWQiLAogICJkYXRhIjogewogICAgImNvbHVtbnMiOiAyNCwKICAgICJyb3dIZWlnaHQiOiAyMCwKICAgICJtYXhXaWR0aCI6IDE0MDAsCiAgICAiYm9yZGVyZWQiOiB0cnVlLAogICAgImNlbGxzIjogWwogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDAsCiAgICAgICAgICAxMiwKICAgICAgICAgIDIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgMiwKICAgICAgICAgIDEyLAogICAgICAgICAgMTAKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgMTIsCiAgICAgICAgICAxMiwKICAgICAgICAgIDI4CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDQwLAogICAgICAgICAgMTIsCiAgICAgICAgICA4CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDQ4LAogICAgICAgICAgMTIsCiAgICAgICAgICAxMgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICA2MCwKICAgICAgICAgIDEyLAogICAgICAgICAgNgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICA2NiwKICAgICAgICAgIDEyLAogICAgICAgICAgMTQKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgODAsCiAgICAgICAgICAxMiwKICAgICAgICAgIDgKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgODgsCiAgICAgICAgICAxMiwKICAgICAgICAgIDEyCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDEwMCwKICAgICAgICAgIDEyLAogICAgICAgICAgMTIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgMTEyLAogICAgICAgICAgMTIsCiAgICAgICAgICAyMgogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICAxMzQsCiAgICAgICAgICAxMiwKICAgICAgICAgIDE0CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMCwKICAgICAgICAgIDE0OCwKICAgICAgICAgIDEyLAogICAgICAgICAgMTIKICAgICAgICBdCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAicG9zaXRpb24iOiBbCiAgICAgICAgICAwLAogICAgICAgICAgMTYwLAogICAgICAgICAgMTIsCiAgICAgICAgICAxNAogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDAsCiAgICAgICAgICAxNzQsCiAgICAgICAgICAxMiwKICAgICAgICAgIDIyCiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMTIsCiAgICAgICAgICAwLAogICAgICAgICAgMTIsCiAgICAgICAgICA0CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogWwogICAgICAgICAgMTIsCiAgICAgICAgICA0LAogICAgICAgICAgMTIsCiAgICAgICAgICAzOAogICAgICAgIF0KICAgICAgfSwKICAgICAgewogICAgICAgICJwb3NpdGlvbiI6IFsKICAgICAgICAgIDEyLAogICAgICAgICAgNDIsCiAgICAgICAgICAxMiwKICAgICAgICAgIDM4CiAgICAgICAgXQogICAgICB9LAogICAgICB7CiAgICAgICAgInBvc2l0aW9uIjogbnVsbAogICAgICB9CiAgICBdCiAgfQp9Cg==",
    auto_download=["html"],
)


@app.cell(column=0)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Iterators in ngio

    **ngio iterators** let you process large images region-by-region without loading
    everything into RAM at once.

    ### Goals of this notebook:
    - Understand why iterators are needed and how the builder pattern works
    - Use `ImageProcessingIterator` for stateless transforms (e.g. gaussian blur)
    - Use `SegmentationIterator` for stateful processing (e.g. instance segmentation)
    - Control iteration with ROI tables and axis broadcasting
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 Why iterators?

    Loading a large microscopy image into RAM is often impractical.
    ngio's **iterator pattern** solves this: it splits the image into regions,
    feeds each patch to your processing function, and writes results back —
    without ever holding the full image in memory.

    ngio ships four iterator types:

    | Iterator | Use case | Execution method |
    |---|---|---|
    | `ImageProcessingIterator` | Stateless transform (blur, normalise, …) | `.map_as_numpy(fn)` |
    | `MaskedSegmentationIterator` | Transform restricted to a masked region | `.map_as_numpy(fn)` |
    | `SegmentationIterator` | Segmentation producing integer label masks | `.iter_as_numpy()` |
    | `FeatureExtractorIterator` | Read-only per-object measurements | `.iter_as_numpy()` |

    All iterators share the same **builder pattern**:

    ```python
    iterator = SomeIterator(input_image=..., output=...)
        .product(roi_table)   # restrict to spatial regions
        .by_zyx()             # broadcast over remaining axes

    iterator.map_as_numpy(my_fn)   # stateless: applies fn, writes back, consolidates
    # — or —
    for patch, writer in iterator.iter_as_numpy():   # stateful: manual write-back
        result = my_stateful_fn(patch)
        writer(patch=result)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 Setup

    We reuse the same `CardiomyocyteTinyMip` sample dataset as notebook 1 —
    a single well image with one DAPI channel, one Z-plane (MIP), and an FOV ROI table.
    We derive two empty output containers to receive the processed results.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import ngio
    from ngio.utils import download_ome_zarr_dataset

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    hcs_path = download_ome_zarr_dataset("CardiomyocyteTinyMip", download_dir=data_dir)
    image_path = hcs_path / "B" / "03" / "0"
    ome_zarr = ngio.open_ome_zarr_container(image_path)

    image = ome_zarr.get_image()
    fov_table = ome_zarr.get_roi_table("FOV_ROI_table")

    print(f"Image shape : {image.shape}")
    print(f"Axes        : {image.axes}")
    print(f"Channels    : {image.channel_labels}")
    print(f"FOV regions : {[r.name for r in fov_table.rois()]}")
    return data_dir, fov_table, image, ome_zarr


@app.cell
def _(data_dir, ome_zarr):
    blurred_zarr = ome_zarr.derive_image(data_dir / "blurred.zarr", overwrite=True)
    blurred_image = blurred_zarr.get_image()
    print(f"Derived blurred container: {blurred_zarr}")
    return (blurred_image,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 ImageProcessingIterator — stateless transforms

    `ImageProcessingIterator` is the right tool when the output for each patch
    depends only on the patch itself — no cross-patch state.

    ### 3.1 Define the transform

    Any `f(patch: np.ndarray) → np.ndarray` works.
    The patch shape follows the `axes_order` you specify in the iterator.
    """)
    return


@app.cell
def _():
    from skimage.filters import gaussian

    def gaussian_blur(patch):
        return gaussian(patch, sigma=2, preserve_range=True).astype(patch.dtype)

    return (gaussian_blur,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 Build and run

    `.product(table)` restricts iteration to the ROIs in the table.
    `.by_zyx(strict=False)` splits each ROI by Z-plane so a 2-D function can
    process 3-D data one slice at a time. When `strict=True` (default), it raises
    if the image is 2-D (Z = 1); use `strict=False` for MIP or single-plane data.

    `map_as_numpy` applies the function, writes results back, and
    **consolidates the output pyramid automatically** — no `consolidate()` call needed.
    """)
    return


@app.cell
def _(blurred_image, fov_table, gaussian_blur, image):
    from ngio.experimental.iterators import ImageProcessingIterator

    blur_iterator = (
        ImageProcessingIterator(
            input_image=image,
            output_image=blurred_image,
            axes_order=["c", "z", "y", "x"],
        )
        .product(fov_table)
        .by_zyx(strict=False)
    )
    blur_iterator.map_as_numpy(gaussian_blur)
    print(f"Done — processed {len(blur_iterator.rois)} region(s)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3 Broadcasting and validation

    The builder methods control how the ROI list is expanded:

    | Method | Effect |
    |---|---|
    | `.product(roi_table)` | Cartesian product with table ROIs — iterate each FOV |
    | `.by_zyx(strict=False)` | Split each ROI into individual Z-planes (`strict=True` raises if Z = 1) |
    | `.by_yx()` | Split into individual YX planes (drops both Z and T broadcasting) |
    | `.by_chunks()` | Sub-divide ROIs to align with zarr chunk boundaries |

    Before running a long job you can assert non-overlapping coverage:

    ```python
    iterator.require_no_regions_overlap()  # raises if any pixel is covered twice
    iterator.require_no_chunks_overlap()   # raises if any zarr chunk is touched twice
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 SegmentationIterator — stateful iteration

    Segmentation must produce **globally unique label IDs** across tiles.
    `map_as_numpy` cannot carry state between patches, so we use `iter_as_numpy()`
    instead — it yields `(data, writer)` tuples so we can track the running
    `max_label` and offset each tile's IDs to avoid collisions.

    ### 4.1 Define the segmentation function
    """)
    return


@app.cell
def _():
    import numpy as np
    from skimage.filters import threshold_otsu
    from skimage.measure import label as skimage_label

    def otsu_segment(patch, offset=0):
        patch_2d = np.squeeze(patch)
        thresh = threshold_otsu(patch_2d)
        labeled = skimage_label(patch_2d > thresh).astype("int32")
        labeled[labeled > 0] += offset
        return labeled.reshape(patch.shape)

    return (otsu_segment,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 Build and run

    `channel_selection="DAPI"` extracts a single channel so the segmentation
    function receives a `[z, y, x]` array rather than `[c, z, y, x]`.

    The loop pattern:
    1. `iter_as_numpy()` yields `(image_patch, label_writer)` pairs
    2. Apply the segmentation function, passing the current `max_label` as offset
    3. Call `writer(patch=result)` to write the tile result back to the label
    4. Update `max_label` so the next tile starts from a higher ID

    Consolidation (pyramid rebuild) runs automatically when the loop finishes.
    """)
    return


@app.cell
def _(fov_table, image, ome_zarr, otsu_segment):
    from ngio.experimental.iterators import SegmentationIterator

    nuc_label = ome_zarr.derive_label("nuclei_seg", overwrite=True)

    seg_iterator = (
        SegmentationIterator(
            input_image=image,
            output_label=nuc_label,
            channel_selection="DAPI",
            axes_order=["z", "y", "x"],
        )
        .product(fov_table)
        .by_zyx(strict=False)
    )

    max_label = 0
    for image_patch, label_writer in seg_iterator.iter_as_numpy():
        seg_patch = otsu_segment(image_patch, offset=max_label)
        max_label = int(seg_patch.max())
        label_writer(patch=seg_patch)

    print(f"Segmentation complete — {max_label} objects found")
    return (nuc_label,)


@app.cell(column=1)
def _(image, mo):
    raw = image.get_as_numpy(axes_order=["y", "x"], c=0, z=0)
    mo.md(f"**Input image** — shape `{raw.shape}`, dtype `{raw.dtype}`")
    return (raw,)


@app.cell(column=1)
def _(blurred_image, plt, raw):
    blurred_arr = blurred_image.get_as_numpy(axes_order=["y", "x"], c=0, z=0)

    fig_blur, ax_blur = plt.subplots(1, 2, figsize=(12, 5))
    ax_blur[0].imshow(raw, cmap="gray")
    ax_blur[0].set_title("Original DAPI")
    ax_blur[0].axis("off")
    ax_blur[1].imshow(blurred_arr, cmap="gray")
    ax_blur[1].set_title("Blurred DAPI (σ=2)")
    ax_blur[1].axis("off")
    fig_blur.tight_layout()
    fig_blur
    return


@app.cell(column=1)
def _(nuc_label, plt, raw):
    seg_arr = nuc_label.get_as_numpy(axes_order=["y", "x"], z=0)

    fig_seg, ax_seg = plt.subplots(1, 2, figsize=(12, 5))
    ax_seg[0].imshow(raw, cmap="gray")
    ax_seg[0].set_title("Original DAPI")
    ax_seg[0].axis("off")
    ax_seg[1].imshow(seg_arr > 0, cmap="gray")
    ax_seg[1].set_title("Segmentation mask")
    ax_seg[1].axis("off")
    fig_seg.tight_layout()
    fig_seg
    return


@app.cell(column=1)
def _():
    import matplotlib.pyplot as plt

    return (plt,)


if __name__ == "__main__":
    app.run()
