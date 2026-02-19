import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
from .tts import ChirpTTS
from .config import ConfigManager

# Load environment variables
load_dotenv()

config_manager = ConfigManager()

app = typer.Typer(
    help="🚀 GCP Chirp 3 HD TTS CLI Tool",
    rich_markup_mode="rich"
)
console = Console()

def check_dependency(name: str) -> bool:
    """Checks if a command-line tool is installed."""
    return shutil.which(name) is not None

def validate_project_id(cli_project: Optional[str] = None):
    """Checks if a project ID is set in CLI, config or environment."""
    # Precedence: CLI > Config > ENV (Config.get handles ENV if config is empty)
    project_id = cli_project or config_manager.get("project_id")
    
    if not project_id:
        console.print(Panel(
            "[bold red]Google Cloud Project ID is not set![/bold red]\n\n"
            "Please provide it via [bold cyan]--project[/bold cyan], set it via [bold cyan]gcp-chirp config[/bold cyan], "
            "or set the [bold green]GOOGLE_CLOUD_PROJECT[/bold green] environment variable.",
            title="Configuration Error",
            border_style="red"
        ))
        raise typer.Exit(code=1)
    return project_id

@app.command()
def setup():
    """
    Check prerequisites and initialize the tool.
    """
    console.print(Panel("🔍 [bold cyan]Starting Setup Diagnostics[/bold cyan]", border_style="cyan"))
    
    # 1. Check FFmpeg
    with console.status("[bold blue]Checking FFmpeg..."):
        has_ffmpeg = check_dependency("ffmpeg")
    
    if has_ffmpeg:
        console.print("[green]✅ FFmpeg found.[/green]")
    else:
        console.print("[red]❌ FFmpeg NOT found.[/red] Please install it: [bold yellow]brew install ffmpeg[/bold yellow]")

    # 2. Check gcloud CLI
    with console.status("[bold blue]Checking gcloud CLI..."):
        has_gcloud = check_dependency("gcloud")
    
    if has_gcloud:
        console.print("[green]✅ gcloud CLI found.[/green]")
    else:
        console.print("[yellow]⚠️  gcloud CLI not found.[/yellow] It's recommended for authentication.")

    # 3. Handle Authentication
    if has_gcloud:
        if typer.confirm("Do you want to set up Application Default Credentials (ADC) now?"):
            try:
                subprocess.run(["gcloud", "auth", "application-default", "login"], check=True)
                console.print("[green]✅ ADC configured successfully.[/green]")
            except subprocess.CalledProcessError:
                console.print("[red]❌ ADC configuration failed.[/red]")

    # 4. Run Config Wizard
    if typer.confirm("Do you want to run the Configuration Wizard now?"):
        config(show=False)
    
    console.print(Panel("[bold green]Setup Complete![/bold green]", border_style="green"))

@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration")
):
    """
    Configure settings interactively.
    """
    if show:
        table = Table(title="Current Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="green")
        table.add_column("Value", style="yellow")
        
        for k, v in config_manager.all.items():
            display_val = str(v)
            if k == "project_id" and not v:
                env_val = os.environ.get("GOOGLE_CLOUD_PROJECT")
                if env_val:
                    display_val = f"{env_val} [dim](from GOOGLE_CLOUD_PROJECT)[/dim]"
            table.add_row(k, display_val)
        
        console.print(table)
        return

    console.print(Panel("🛠 [bold cyan]Chirp 3 HD Configuration Wizard[/bold cyan]", border_style="cyan"))
    
    # Interactive Prompts
    env_project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    current_project = config_manager.get("project_id") or env_project
    
    project_id = typer.prompt("Google Cloud Project ID", default=current_project)
    default_voice = typer.prompt("Default Chirp Voice", default=config_manager.get("default_voice"))
    default_lang = typer.prompt("Default Language Code", default=config_manager.get("default_language"))
    output_dir = typer.prompt("Default Output Directory", default=config_manager.get("output_dir"))
    auto_play = typer.confirm("Auto-play audio after synthesis?", default=config_manager.get("auto_play"))

    # Save settings
    config_manager.set("project_id", project_id)
    config_manager.set("default_voice", default_voice)
    config_manager.set("default_language", default_lang)
    config_manager.set("output_dir", output_dir)
    config_manager.set("auto_play", auto_play)
    
    config_manager.save()
    from .config import CONFIG_FILE
    console.print(f"\n[bold green]✨ Configuration saved to {CONFIG_FILE}[/bold green]")

@app.command()
def config_reset():
    """
    Reset configuration to defaults.
    """
    if typer.confirm("Are you sure you want to reset all settings to defaults?"):
        config_manager.reset()
        console.print("[bold green]✨ Configuration has been reset to defaults.[/bold green]")

@app.command()
def uninstall():
    """
    Remove local configuration and clean up.
    """
    from .config import CONFIG_DIR
    if CONFIG_DIR.exists():
        console.print(Panel(
            f"[bold red]WARNING:[/bold red] This will permanently delete your configuration at [underline]{CONFIG_DIR}[/underline]",
            title="Cleanup Confirmation",
            border_style="red"
        ))
        if typer.confirm("Are you sure you want to proceed?"):
            shutil.rmtree(CONFIG_DIR)
            console.print("[bold green]✨ Local configuration removed.[/bold green]")
            console.print("[dim]To fully uninstall the tool, run: [bold]uv tool uninstall gcp-chirp[/bold][/dim]")
    else:
        console.print("[yellow]No local configuration found to clean up.[/yellow]")

@app.command()
def list(
    lang: str = typer.Option(None, "--lang", help="Language code (e.g., en-US, es-ES)"),
    project: str = typer.Option(None, "--project", help="GCP Project ID override")
):
    """
    List available Chirp 3 HD voices.
    """
    validate_project_id(project)
    target_lang = lang or config_manager.get("default_language")
    try:
        tts = ChirpTTS()
        with console.status(f"[bold green]Fetching voices for {target_lang}..."):
            voices = tts.list_voices(target_lang)
        
        if not voices:
            console.print(f"[yellow]No Chirp 3 HD voices found for language: {target_lang}[/yellow]")
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
    voice: str = typer.Option(None, "--voice", help="Voice name"),
    output: str = typer.Option(None, "--output", help="Output audio file path"),
    project: str = typer.Option(None, "--project", help="GCP Project ID override"),
    auto_play: Optional[bool] = typer.Option(None, "--play/--no-play", help="Override auto-play setting"),
    creds: str = typer.Option(None, help="Path to GCP Service Account JSON")
):
    """
    Synthesize speech using Chirp 3 HD.
    """
    validate_project_id(project)
    target_voice = voice or config_manager.get("default_voice")
    target_auto_play = auto_play if auto_play is not None else config_manager.get("auto_play")
    # Determine output path
    if output:
        output_path = output
    else:
        from datetime import datetime
        name_template = config_manager.get("output_template").replace("{timestamp}", datetime.now().strftime("%Y%m%d_%H%M%S"))
        output_path = os.path.join(config_manager.get("output_dir"), name_template)

    try:
        tts = ChirpTTS(credentials_path=creds)
        
        console.print(Panel(
            f"[bold blue]Synthesizing:[/bold blue] {text[:50]}{'...' if len(text) > 50 else ''}\n"
            f"[bold green]Voice:[/bold green] {target_voice}\n"
            f"[bold yellow]Output:[/bold yellow] {output_path}",
            title="TTS Synthesis",
            border_style="blue"
        ))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Generating audio...", total=None)
            final_output = tts.synthesize(text, target_voice, output_path)

        console.print(f"[bold green]✨ Success![/bold green] Audio saved to [underline]{final_output}[/underline]")
        
        if target_auto_play:
            console.print("[dim]Playing audio...[/dim]")
            if os.uname().sysname == "Darwin":
                os.system(f"afplay '{final_output}'")
            else:
                os.system(f"play '{final_output}'") # Common on Linux with sox
    except Exception as e:
        console.print(Panel(f"[red]Error:[/red] {str(e)}", title="Failure", border_style="red"))

if __name__ == "__main__":
    app()
