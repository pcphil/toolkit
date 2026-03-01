# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python toolkit of reusable utilities for everyday tasks like image manipulation and base64 encoding/decoding.

## Setup

```bash
uv venv --python 3.12
source .venv/Scripts/activate  # Windows (Git Bash)
pip install -r requirements.txt
```

Dependencies: `pillow`, `vtracer`

## How to Use

Tools are used interactively via `sandbox.ipynb`. Import classes from `src.tools` and call their static methods:

```python
from src.tools.icon_maker import IconMaker
from src.tools.base64_operations import Base64Operations
```

## Architecture

- `src/tools/` — All utility modules live here as classes with `@staticmethod` methods
  - `icon_maker.py` — `IconMaker`: ICO generation from images (with circular crop option), circular border cropping
  - `base64_operations.py` — `Base64Operations`: encode/decode strings or file-like objects to/from base64
- `input/` — Source files for processing
- `output/` — Generated output files (default destination for all tools)
- `sandbox.ipynb` — Interactive notebook for running tools

## Conventions

- Each tool is a class with only static methods (no instance state)
- Default output paths point to `output/` directory
- Tools accept `input_path`/`output_path` parameters with sensible defaults
- File collision is handled via `_get_unique_path` (appends `_1`, `_2`, etc.)
