# 🎼 Conductor Tracks

## Current Track: googlecloud-chirp CLI Tool Development
- **Status**: Active
- **Objective**: Build a Python CLI tool for Google Cloud TTS Chirp 3 HD voices using `uv`.
- **Milestones**:
    - [x] Project Initialization with `uv`
    - [x] Dependency Installation
    - [x] CLI Design (Typer + Rich)
    - [x] Chirp 3 HD Voice Integration
    - [x] Testing & Validation
    - [x] README & Documentation

## Current Track: Configuration System & Testing
- **Status**: In Progress
- **Goal**: Implement `config` command and persistent settings in `~/.googlecloud-chirp/settings.yaml`.
- **Milestones**:
    - [x] Add PyYAML and testing dependencies
    - [x] Implement `src/googlecloud_chirp/config.py` manager
    - [x] Create `config` command wizard in `cli.py`
    - [x] Refactor `say` and `list` to use config defaults
    - [x] Write and run test suite

## Current Track: Setup Experience & Diagnostics
- **Status**: Starting
- **Goal**: Create a `setup` command that automates prerequisite checks and initialization.
- **Milestones**:
    - [x] Implement dependency check (ffmpeg, gcloud)
    - [x] Create `setup` command in `cli.py`
    - [x] Integrated guided authentication (ADC)
    - [x] Auto-invoke `config` wizard during setup

## Current Track: PyPI Readiness & Tool Distribution
- **Status**: Completed
- **Goal**: Prepare the package for PyPI and global distribution as a CLI tool.
- **Milestones**:
    - [x] Add PyPI metadata to `pyproject.toml`
    - [x] Implement internal `uninstall` command for state cleanup
    - [x] Update documentation for `uv tool install`
    - [ ] Perform trial build with `uv build`
