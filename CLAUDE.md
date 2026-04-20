# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

nzshm-common is a shared Python library for the New Zealand National Seismic Hazard Model (NSHM) ecosystem. It provides location handling, grid operations, geometry utilities, and compression helpers used across NSHM projects. Published on PyPI as `nzshm-common`.

## Development Setup

```bash
uv sync --all-extras    # Install with all optional dependencies (e.g., Shapely)
```

## Common Commands

```bash
# Testing
uv run pytest tests                          # Run all tests
uv run pytest tests/test_coded_location.py   # Run a single test file
uv run pytest -k "test_name"                 # Run tests matching keyword
uv run tox                                   # Full matrix (py310, py311, py312 + lint + format + audit)
uv run tox -e py312                          # Single Python version

# Linting & Formatting
uv run tox -e lint                           # ruff check + mypy
uv run tox -e format                         # ruff format check
uv run ruff format .                         # Auto-format
uv run ruff check --select I --fix .         # Sort imports

# Security
uv run tox -e audit                          # pip-audit + safety

# Docs
uv run mkdocs serve                          # Local docs preview
```

## Code Style

- **Line length**: 120 (black, isort, flake8 all use 120)
- **Formatter**: black with `skip-string-normalization=true` (preserves quote style)
- **Import sorting**: isort with vertical hanging indent (multi_line_output=3), trailing commas
- **Docstrings**: Google convention (flake8-docstrings configured but D rules currently ignored)

## Architecture

**CodedLocation** (`nzshm_common/location/coded_location.py`) is the central abstraction — a lat/lon pair quantized to a grid resolution (default 0.001). It is a frozen dataclass, hashable and sortable (N→S, then W→E). The `code` property returns a `"lat~lon"` string identifier. It uses `__post_init__` (not `__init__`) for Pydantic BaseModel compatibility.

**CodedLocationBin** groups CodedLocations at a coarser resolution via `bin_locations()`.

**Location data** (`nzshm_common/location/`) provides named NZ location lookups (`location_by_id()`, `get_locations()`) and predefined location lists (NZ, NZ2, SRWG214, etc.) backed by JSON/CSV resource files.

**RegionGrid** (`nzshm_common/grids/region_grid.py`) is an enum of predefined NZ regional grids with `load_grid()` and `get_location_grid()` helpers.

**Geometry** (`nzshm_common/geometry/`) requires the optional `shapely` dependency. Provides hexagon/square tile creation, backarc polygon, and point-in-polygon checks.

**Compression** (`nzshm_common/util/compression.py`) provides ZIP+base64 string compression utilities.

## Versioning & Release

Uses bump2version (config in `.bumpversion.cfg`). Release by bumping version and pushing a `v*` tag — CI publishes to PyPI and deploys docs automatically.
