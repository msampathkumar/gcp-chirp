# 🎙️ googlecloud-chirp

A premium CLI tool for working with **Google Cloud Text-to-Speech Chirp 3 HD** voices. Chirp 3 HD is a new generation of expressive, high-fidelity voices powered by Google's latest LLMs.

## 📋 Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **FFmpeg**: Required for audio processing.
    ```bash
    # macOS
    brew install ffmpeg
    ```
2.  **Google Cloud Project**:
    - Enable the **Text-to-Speech API**.
    - Set up **Application Default Credentials (ADC)**. Follow the [official documentation](https://docs.cloud.google.com/docs/authentication/application-default-credentials).
    - *Note*: You may need to perform a one-time setup for the `gcloud` CLI:
      ```bash
      gcloud auth application-default login
      ```

## 🚀 Features

- **Expressive Synthesis**: High-fidelity audio with natural intonation.
- **Voice Listing**: Easily list available Chirp 3 HD voices across languages.
- **Modern CLI**: Beautiful output powered by `rich` and `typer`.
- **Managed by uv**: Lightning fast dependency management.

## 📦 Installation

This project uses `uv`. Ensure you have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd googlecloud-chirp
uv sync
```

## 🔑 Authentication

The tool uses Google Cloud **Application Default Credentials (ADC)** by default.

1.  **ADC (Recommended)**: Run the following command if you haven't already:
    ```bash
    gcloud auth application-default login
    ```
2.  **Service Account Key**: If using a service account JSON:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"
    ```
3.  **CLI Option**: Alternatively, pass the path directly via the `--creds` option in the `say` command.

## 🛠 Usage

### Configuration Precedence
The tool follows a strict precedence for settings:
1.  **CLI Flags**: (e.g., `--project`, `--voice`, `--play`) always win.
2.  **Config File**: (`~/.googlecloud-chirp/settings.yaml`).
3.  **Environment Variables**: (e.g., `GOOGLE_CLOUD_PROJECT`).

### ⚙️ Configuration Commands

#### Interactive Setup
Set your default project, voice, and output preferences:
```bash
uv run googlecloud-chirp config
```

#### View Current Configuration
```bash
uv run googlecloud-chirp config --show
```

#### Reset Configuration
Reset all settings to factory defaults:
```bash
uv run googlecloud-chirp config-reset
```

### 📋 Action Commands

#### List Voices
List available voices for a language (uses default language if omitted):
```bash
uv run googlecloud-chirp list --project my-temporary-project
```

#### Synthesize Speech
Convert text to audio with overrides:
```bash
uv run googlecloud-chirp say "Hello, I am synthesized using a specific project and voice!" --voice en-US-Chirp3-HD-Charon --project my-project --play
```

*Note: Files are saved in the configured `output_dir` with a timestamped filename unless `--output` is provided.*

## 🏗 Track Status

Managed via `conductor/tracks.md`.

---
*Built with ❤️ for the Empire.*
