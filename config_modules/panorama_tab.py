from panos.panorama import Template

from rich.progress import track
from rich.console import Console

def template_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    # loop through all the templates
    for template in track(config_facts):
        # define the template configuration
        configuration = Template(f"{template['template_name']}")
        try:
            pano.add(configuration).create()
            success_messages.append(f"TEMPLATE:{configuration} successfully configured.")
        except Exception as msg:
            failure_messages.append(f"TEMPLATE:{template['template_name']} failed to configure with message {msg}.")

    # return the success and failure messages
    return success_messages, failure_messages