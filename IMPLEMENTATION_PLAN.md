# 🧪 Implementation & Testing Plan: gcp-chirp

This plan outlines the steps for finalizing the implementation, expanding the test suite, and preparing for PyPI release.

## 🚀 Phase 1: Core Implementation Refinement
- [x] **Error Handling**: Add more specific exception handling for network issues and API quota limits in `tts.py`.
- [x] **Shell Completion**: Ensure `typer` shell completion is easy to install via `setup` command.
- [x] **Input Support**: Allow synthesizing text from a file (e.g., `gcp-chirp say --file input.txt`).

## 🧪 Phase 2: Comprehensive Testing
- **Directory**: `tests/`
- **Milestones**:
    - [x] **Config Tests**: `tests/test_config.py` (Completed)
    - [x] **TTS Client Mocking**: `tests/test_tts.py` - Mock the Google Cloud TTS client to test synthesis logic without burning credits.
    - [x] **CLI Integration Tests**: `tests/test_cli.py` - Test the command-line interface using `typer.testing.CliRunner`.
    - [ ] **E2E Dry Run**: Create a script to simulate a full user journey from `setup` -> `config` -> `say`.

## 📦 Phase 3: Distribution
- [ ] **Build Check**: Run `uv build` to verify dist files.
- [ ] **Metadata Scan**: Review `pyproject.toml` keywords and descriptions.
- [ ] **PyPI Upload**: (When ready) Use `uv publish`.

---
*Status: Initializing Phase 2*
