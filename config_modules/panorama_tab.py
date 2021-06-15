from panos.panorama import Template

from rich.progress import track
from rich.console import Console

console = Console()


def template_configuration(config_facts, logfile, pano) -> None:
    # loop through all the templates
    for template in track(config_facts):
        # define the template configuration
        configuration = Template(f"{template['template_name']}")
        try:
            pano.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: TEMPLATE:{configuration} successfully configured."
            )
            logfile.write(
                f" Successful: TEMPLATE:{configuration} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: TEMPLATE:{template['template_name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: TEMPLATE:{template['template_name']} failed to configure with message {msg}.\n"
            )
