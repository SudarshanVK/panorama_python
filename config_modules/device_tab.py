from panos.panorama import Template
from panos.device import Vsys

from rich.console import Console
from rich.progress import track
console = Console()

def vsys_configuration(config_facts, template_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    # print (config_facts)
    #! This configuration will delete vsys1 in each template that is newly created in this design
    for template in template_facts:
        try:
            parent_template = Template(f"{template['template_name']}")
            template_config = pano.add(parent_template)
            template_config.add(Vsys("vsys1")).delete()
            success_messages.append(f"VSYS:vsys1 successfully deleted under TEMPLATE {parent_template}.")
        except Exception as msg:
            failure_message.append(f"VSYS:vsys1 failed to deleted under TEMPLATE {parent_template} with message {msg}.")
        
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
            success_messages.append(f"VSYS:{vsys_config['name']} successfully created.")
        except Exception as msg:
            failure_message.append(f"VSYS:{vsys_config['name']} failed with message {msg}.")

    # update the vsys with visible vsys configuration
    for vsys_config in vsys_visible_vsys_defined:
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
            success_messages.append(f"VSYS:{vsys_config['name']} updated successfully with with visible_vsys config")
        except Exception as msg:
            failure_messages.append(f"VSYS:{vsys_config['name']} updating visual_vsys failed with message {msg}"
            )

    return success_messages, failure_messages