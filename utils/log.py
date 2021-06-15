from rich.console import Console

console = Console()


def log_messages(success_messages, failure_messages, logfile) -> None:
    for message in success_messages:
        console.print(f"[bold green]:thumbs_up: {message}[/bold green]")
        logfile.write(f"Successful: {message}\n")
    for message in failure_messages:
        console.print(f"[bold red]:thumbs_down: {message}[/bold red]")
        logfile.write(f"Failed: {message}\n")
