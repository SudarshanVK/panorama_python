from panos.panorama import Panorama

from rich.console import Console

console = Console()


def panorama_connect(logfile, device, username, password):

    try:
        p_rama = Panorama(device, username, password)
    except:
        console.print(
            f":thumbs_down: Unable to connect to device", style="bold red"
        )
        logfile.write(f"Unable to connect to device\n")
        exit(1)
    return p_rama
