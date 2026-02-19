---
name: ChirpTTS
description: High-fidelity voice synthesis using Google Cloud Chirp 3 HD.
---
# 🎙️ ChirpTTS Skill

## Context
You are an AI Agent with the ability to generate premium, high-fidelity speech using Google Cloud's Chirp 3 HD model. Use this skill to communicate with humans or create audio content with natural intonation.

## Requirements
- `gcp-chirp` CLI tool installed.
- Google Cloud Project with Text-to-Speech API enabled.
- Authentication configured via `gcp-chirp setup`.

## Capability: Synthesize Speech
Use the `gcp-chirp say` command to convert text to speech.

### Usage
```bash
# Basic synthesis
gcp-chirp say "Hello, I am using Chirp 3 HD voices."

# Synthesis from a file
gcp-chirp say --file script.txt

# Specify a specific voice
gcp-chirp say "Custom voice selection" --voice en-US-Chirp3-HD-Charon

# Synthesis for a specific project
gcp-chirp say "Synthesis with project override" --project my-gcp-project
```

## Capability: List Voices
Discover available expressive voices for different languages.

### Usage
```bash
# List US English voices
gcp-chirp list --lang en-US

# List Spanish voices
gcp-chirp list --lang es-ES
```

## Best Practices
1. **Punctuation**: Use proper commas and periods to help the LLM-based model understand natural pauses.
2. **Setup**: Always ensure `gcp-chirp setup` has been run to verify dependencies like FFmpeg.
3. **Defaults**: Set your preferred voice in `gcp-chirp config` to simplify subsequent calls.
