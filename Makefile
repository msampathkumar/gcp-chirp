.PHONY: install uninstall test build clean setup help gemini-install gemini-uninstall agent-onboard

help:
	@echo "Available commands:"
	@echo "  make install         - Install the tool globally using uv tool install"
	@echo "  make uninstall       - Uninstall the tool globally"
	@echo "  make test            - Run all tests using pytest"
	@echo "  make build           - Build source and wheel distributions"
	@echo "  make clean           - Remove build artifacts and cache"
	@echo "  make setup           - Run the internal setup wizard"
	@echo "  make gemini-install  - Install the ChirpTTS skill for Gemini Agent"
	@echo "  make gemini-uninstall - Remove the ChirpTTS skill for Gemini Agent"
	@echo "  make agent-onboard   - Onboard an AI agent to use this tool"

install:
	uv tool install . --force

uninstall:
	uv tool uninstall gcp-chirp

test:
	uv run pytest

build:
	uv build

clean:
	rm -rf dist/ .pytest_cache/ .venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +

setup:
	uv run gcp-chirp setup

gemini-install:
	@mkdir -p ~/.gemini/skills/chirp-tts
	@cp -r agents/skills/gemini/* ~/.gemini/skills/chirp-tts/
	@echo "✨ ChirpTTS skill installed to ~/.gemini/skills/chirp-tts/"

gemini-uninstall:
	@rm -rf ~/.gemini/skills/chirp-tts
	@echo "🗑️ ChirpTTS skill removed from ~/.gemini/skills/chirp-tts/"

agent-onboard:
	@echo "🤖 [bold cyan]Agent Onboarding: gcp-chirp[/bold cyan]"
	@echo "--------------------------------------------------"
	@echo "Welcome, Agent. You have been granted access to the Chirp 3 HD voice synthesis system."
	@echo ""
	@echo "1. Capabilities:"
	@echo "   - Synthesize high-fidelity speech from text or files."
	@echo "   - List expressive voices powered by Google's latest LLMs."
	@echo ""
	@echo "2. Your Interface:"
	@echo "   - Primary Command: 'gcp-chirp say <text>'"
	@echo "   - File Input: 'gcp-chirp say --file <path>'"
	@echo "   - Voice Discovery: 'gcp-chirp list --lang <lang_code>'"
	@echo ""
	@echo "3. Integration:"
	@echo "   - Your skill definition is located in 'agents/skills/gemini/SKILL.md'."
	@echo "   - Run 'make gemini-install' to add this capability to your core system."
	@echo ""
	@echo "4. Mission Guidelines:"
	@echo "   - Use natural punctuation for best results."
	@echo "   - Always check dependencies with 'gcp-chirp setup' if unsure."
	@echo "--------------------------------------------------"
