# ngio Workshop

Hands-on workshop materials to get started with [ngio](https://biovisioncenter.github.io/ngio). ngio is a Python library designed to simplify bioimage analysis workflows, offering an intuitive interface for working with OME-Zarr files.

Each notebook is self-contained: it declares its own dependencies inline and marimo uses [uv](https://docs.astral.sh/uv/) to create an isolated environment automatically.

## Prerequisites

[uv](https://docs.astral.sh/uv/getting-started/installation/) — that's it.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Running a notebook

```bash
uvx marimo edit --sandbox notebooks/<notebook>.py
```

On first run uv will create an isolated environment for the notebook and install its dependencies. This takes a minute; subsequent runs are instant.

## Workshop modules

| Module | Topic |
|--------|-------|
| [1 — Introduction to ngio](notebooks/1_ngio_basics.py) | OME-Zarr containers, images, labels, and tables |

## Documentation

You can find view a static version of the notebooks in the [documentation](https://biovisioncenter.github.io/ngio-workshop/).

Or you can build the documentation locally with:

```bash
uv run docs/build.py
```
