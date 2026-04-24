# ngio Workshop

Hands-on workshop materials for [ngio](https://github.com/fractal-analytics-platform/ngio), a Python library for reading and writing OME-Zarr / NGFF bioimages. Notebooks are built with [marimo](https://marimo.io) for an interactive, reproducible experience.

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

## Documentation

Live notebooks (read-only): https://&lt;your-org&gt;.github.io/ngio-workshop/

To build docs locally:

```bash
uv run docs/build.py
```

## Workshop modules

| Module | Topic |
|--------|-------|
| [1 — Introduction to ngio](notebooks/1_ngio_basics.py) | OME-Zarr containers, images, labels, and tables |
