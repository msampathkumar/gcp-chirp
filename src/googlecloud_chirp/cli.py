import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import os
from pathlib import Path
from dotenv import load_dotenv
from .tts import ChirpTTS

# Load environment variables
load_dotenv()

app = typer.Typer(
    help="🚀 Google Cloud Chirp 3 HD TTS CLI Tool",
    rich_markup_mode="rich"
)
console = Console()

@app.command()
def list(
    lang: str = typer.Option("en-US", help="Language code (e.g., en-US, es-ES)")
):
    """
    列出可用的 Chirp 3 HD 语音 (List available Chirp 3 HD voices)
    """
    try:
        tts = ChirpTTS()
        with console.status("[bold green]Fetching voices..."):
            voices = tts.list_voices(lang)
        
        if not voices:
            console.print(f"[yellow]No Chirp 3 HD voices found for language: {lang}[/yellow]")
            return

        table = Table(title=f"Chirp 3 HD Voices ({lang})", show_header=True, header_style="bold magenta")
        table.add_column("Voice Name", style="cyan")
        
        for voice in voices:
            table.add_row(voice)
        
        console.print(table)
    except Exception as e:
        console.print(Panel(f"[red]Error:[/red] {str(e)}", title="Failure", border_style="red"))

@app.command()
def say(
    text: str = typer.Argument(..., help="Text to synthesize"),
    voice: str = typer.Option("en-US-Chirp3-HD-A", help="Voice name"),
    output: str = typer.Option("output.mp3", help="Output audio file path"),
    creds: str = typer.Option(None, help="Path to GCP Service Account JSON")
):
    """
    使用 Chirp 3 HD 合成语音 (Synthesize speech using Chirp 3 HD)
    """
    try:
        tts = ChirpTTS(credentials_path=creds)
        
        console.print(Panel(
            f"[bold blue]Synthesizing:[/bold blue] {text[:50]}{'...' if len(text) > 50 else ''}\n"
            f"[bold green]Voice:[/bold green] {voice}\n"
            f"[bold yellow]Output:[/bold yellow] {output}",
            title="TTS Synthesis",
            border_style="blue"
        ))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Generating audio...", total=None)
            final_output = tts.synthesize(text, voice, output)

        console.print(f"[bold green]✨ Success![/bold green] Audio saved to [underline]{final_output}[/underline]")
    except Exception as e:
        console.print(Panel(f"[red]Error:[/red] {str(e)}", title="Failure", border_style="red"))

if __name__ == "__main__":
    app()
