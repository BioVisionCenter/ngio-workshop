# ngio Workshop

Hands-on workshop materials to get started with [ngio](https://biovisioncenter.github.io/ngio). ngio is a Python library designed to simplify bioimage analysis workflows, offering an intuitive interface for working with OME-Zarr files.

Each notebook is self-contained: it declares its own dependencies inline and marimo uses [uv](https://docs.astral.sh/uv/) to create an isolated environment automatically.

## Running locally

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

On Unix-like systems (Linux, macOS):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
and, on Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Running a notebook

```bash
uvx marimo edit --sandbox notebooks/<notebook>.py
```

On first run uv will create an isolated environment for the notebook and install its dependencies. This takes a minute; subsequent runs are instant.

## Running in the cloud (no installation)

Click the **Open in molab** badge next to any notebook in the table below to run it in your browser via [molab](https://molab.marimo.io). No local setup required — a free molab account is needed to execute cells.

> Warning: we observed some issues when leaving a molab notebook idle for a long time, or when going in and out of the notebook. If you encounter errors close tha tab re-open the notebook.

## Following along with the static documentation

A static version of the notebooks is available in the [documentation](https://biovisioncenter.github.io/ngio-workshop/). You can follow along with the examples there, but you won't be able to modify and execute cells.

## Workshop modules

| Module | Topic | Open in molab | Static HTML |
|--------|-------|---|---|
| [1 — Introduction](notebooks/1_ngio_basics.py) | OME-Zarr containers, images, labels, and tables | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/BioVisionCenter/ngio-workshop/blob/main/notebooks/1_ngio_basics.py) | [View](https://biovisioncenter.github.io/ngio-workshop/1_ngio_basics.html) |
| [2 — Iterators](notebooks/2_iterators.py) | Declarative image processing iterators | [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/BioVisionCenter/ngio-workshop/blob/main/notebooks/2_iterators.py) | [View](https://biovisioncenter.github.io/ngio-workshop/2_iterators.html) |

## Slides

You can find the slides for the workshop as PDF [here](https://drive.google.com/file/d/1IRxC4qD2LvIBcGzyqdWbFsb1DHFXVbIC/view?usp=sharing).
