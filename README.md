# ngio Workshop

Hands-on workshop materials to get started with [ngio](https://biovisioncenter.github.io/ngio). ngio is a Python library designed to simplify bioimage analysis workflows, offering an intuitive interface for working with OME-Zarr files.

Each notebook is self-contained: it declares its own dependencies inline and marimo uses [uv](https://docs.astral.sh/uv/) to create an isolated environment automatically.

## Running in the cloud (no installation)

Click the **Open in molab** badge next to any notebook in the table below to run it in your browser via [molab](https://molab.marimo.io). No local setup required — a free molab account is needed to execute cells.

## Running locally

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Running a notebook

```bash
uvx marimo edit --sandbox notebooks/<notebook>.py
```

On first run uv will create an isolated environment for the notebook and install its dependencies. This takes a minute; subsequent runs are instant.


## Following along with the static documentation

A static version of the notebooks is available in the [documentation](https://biovisioncenter.github.io/ngio-workshop/). You can follow along with the examples there, but you won't be able to modify and execute cells.

## Workshop modules

| Module | Topic | Open in molab | Static HTML |
|--------|-------|---|---|
| [1 — Introduction to ngio](notebooks/1_ngio_basics.py) | OME-Zarr containers, images, labels, and tables | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/BioVisionCenter/ngio-workshop/blob/main/notebooks/1_ngio_basics.py) | [View](https://biovisioncenter.github.io/ngio-workshop/1_ngio_basics.html) |
| [2 — Iterators in ngio](notebooks/2_iterators.py) | Iterating over images region-by-region without loading into RAM | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/BioVisionCenter/ngio-workshop/blob/main/notebooks/2_iterators.py) | [View](https://biovisioncenter.github.io/ngio-workshop/2_iterators.html) |

