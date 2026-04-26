import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Rectangle

from ngio import OmeZarrContainer

BVC_TEAL = "#3DBDB8"

_cycled = np.random.rand(1000, 3)
_cycled[0] = [0, 0, 0]  # background is always black
LABEL_CMAP = colors.ListedColormap(_cycled)


def _add_scale_bar(ax, pixel_size_um, length_um=50.0):
    bar_px = length_um / pixel_size_um
    x_max = ax.get_xlim()[1]
    y_max = ax.get_ylim()[0]  # imshow origin='upper': bottom == max
    pad_x = 0.04 * x_max
    pad_y = 0.04 * y_max
    x0 = x_max - pad_x - bar_px
    y0 = y_max - pad_y
    ax.plot(
        [x0, x0 + bar_px],
        [y0, y0],
        color="white",
        linewidth=3,
        solid_capstyle="butt",
    )
    ax.text(
        x0 + bar_px / 2,
        y0 - 0.015 * y_max,
        f"{length_um:g} µm",
        color="white",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )


def plot_image(
    ome_zarr: OmeZarrContainer,
    path: str = "0",
    title: str = "",
    label: str | None = None,
    roi_table: str | None = None,
    figsize: tuple[float, float] = (8, 8),
    scale_bar_um: float | None = 50.0,
    **kwargs,
):
    image = ome_zarr.get_image(path=path)
    img = image.get_as_numpy(**kwargs)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(img, cmap="gray")
    ax.set_title(title)
    ax.axis("off")

    if label is not None:
        lbl = ome_zarr.get_label(label, path=path)
        label_kwargs = {k: v for k, v in kwargs.items() if k != "channel_selection"}
        lbl_img = lbl.get_as_numpy(**label_kwargs)
        ax.imshow(lbl_img, cmap=LABEL_CMAP, interpolation="nearest", alpha=0.5)

    if roi_table is not None:
        table = ome_zarr.get_generic_roi_table(roi_table)
        for roi in table.rois():
            px_roi = roi.to_pixel(pixel_size=image.pixel_size)
            xs, ys = px_roi.get("x"), px_roi.get("y")
            if xs is None or ys is None or xs.start is None or ys.start is None:
                continue
            ax.add_patch(
                Rectangle(
                    (xs.start, ys.start),
                    xs.length,
                    ys.length,
                    fill=False,
                    edgecolor=BVC_TEAL,
                    linewidth=0.8,
                )
            )

    if scale_bar_um is not None and getattr(image.pixel_size, "x", None):
        _add_scale_bar(ax, pixel_size_um=image.pixel_size.x, length_um=scale_bar_um)

    fig.tight_layout()
    plt.show()


def compare_containers(orig, deriv):
    attrs = ("levels", "level_paths", "is_3d", "channel_labels")
    rows = [
        "| Attribute | Original | Derived |  |",
        "|---|---|---|---:|",
    ]
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
