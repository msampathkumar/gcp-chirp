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
