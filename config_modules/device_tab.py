from panos.panorama import Template
from panos.device import Vsys

from rich.console import Console
from rich.progress import track

console = Console()


def vsys_configuration(config_facts, template_facts, logfile, pano) -> None:
    #! This configuration will delete vsys1 in each template that is newly created in this design
    for template in track(template_facts):
        try:
            parent_template = Template(f"{template['template_name']}")
            template_config = pano.add(parent_template)
            template_config.add(Vsys("vsys1")).delete()
            console.print(
                f"[bold green] :thumbs_up: VSYS: vsys1 successfully deleted under TEMPLATE: {parent_template}."
            )
            logfile.write(
                f" Successful: VSYS: vsys1 successfully deleted under TEMPLATE: {parent_template}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: VSYS: vsys1 failed to deleted under TEMPLATE: {parent_template} with message {msg}."
            )
            logfile.write(
                f" Failed: VSYS: vsys1 failed to deleted under TEMPLATE: {parent_template} with message {msg}.\n"
            )

    # create a separate list of vsys configuration that has a visible vsys defined
    vsys_visible_vsys_defined = []
    for vsys_config in track(config_facts):
        if "visible_vsys" in vsys_config:
            vsys_visible_vsys_defined.append(vsys_config.copy())
            vsys_config.pop("visible_vsys")
            # print (vsys_config)
        # define configuration tree
        parent_template = Template(f"{vsys_config['template']}")
        # pop the template name to create a dictionary of vsys configuration
        vsys_config.pop("template")
        # Generate vsys configuration
        configuration = Vsys(**vsys_config)
        try:
            template_config = pano.add(parent_template)
            template_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: VSYS: {vsys_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: VSYS: {vsys_config['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: VSYS: {vsys_config['name']} configuration failed with message {msg}."
            )
            logfile.write(
                f" Failed: VSYS: {vsys_config['name']} configuration failed with message {msg}.\n"
            )

    # update the vsys with visible vsys configuration
    for vsys_config in track(vsys_visible_vsys_defined):
        # print (vsys_config)
        # define configuration tree
        parent_template = Template(f"{vsys_config['template']}")
        # pop the template name to create a dictionary of vsys configuration
        vsys_config.pop("template")
        # Generate vsys configuration
        configuration = Vsys(**vsys_config)
        try:
            template_config = pano.add(parent_template)
            template_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: VSYS: {vsys_config['name']} updated successfully with visible_vsys config"
            )
            logfile.write(
                f" Successful: VSYS: {vsys_config['name']} updated successfully with visible_vsys config.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: VSYS: {vsys_config['name']} updating visual_vsys failed with message {msg}"
            )
            logfile.write(
                f" Failed: VSYS: {vsys_config['name']} updating visual_vsys failed with message {msg}.\n"
            )
