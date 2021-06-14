from panos.panorama import Template
from panos.device import Vsys
from panos.network import VirtualRouter
from panos.network import Zone
from panos.network import AggregateInterface
from panos.network import EthernetInterface
from panos.network import Layer3Subinterface
from panos.network import LoopbackInterface
from panos.network import TunnelInterface
from panos.network import ManagementProfile
from panos.network import StaticRoute

import json
from rich.progress import track

def management_profile_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for profile_configuration in track(config_facts):
        # print (profile_configuration)
        # define configuration tree
        template_parent = Template(f"{profile_configuration['template']}")
        # pop the template name to create a dictionary of aggregate interface configuration
        profile_configuration.pop("template")
        # generate configuration
        configuration = ManagementProfile(**profile_configuration)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # configure aggregate interfaces
            template_config.add(configuration).create()
            success_messages.append(f"MANAGEMENT PROFILE:{profile_configuration['name']} successfully configured.")
        except Exception as msg:
            failure_messages.append(f"MANAGEMENT PROFILE:{profile_configuration['name']} failed to configure with message {msg}\n"
            )
    
    # return the success and failure messages
    return success_messages, failure_messages


def aggregate_interface_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for interface_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{interface_config['template']}")
        # pop the template name to create a dictionary of aggregate interface configuration
        interface_config.pop("template")
        # generate configuration
        configuration = AggregateInterface(**interface_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # configure aggregate interfaces
            template_config.add(configuration).create()
            success_messages.append(f"AGGREGATE INTERFACE:{interface_config['name']} successfully configured."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: AGGREGATE INTERFACE:{interface_config['name']} failed to configure with message {msg}\n"
            )
            
    # return the success and failure messages
    return success_messages, failure_messages

def ethernet_interface_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for interface_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{interface_config['template']}")
        # pop the template name to create a dictionary of ethernet interface configuration
        interface_config.pop("template")
        # define configuration
        configuration = EthernetInterface(**interface_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # configure aggregate interfaces
            template_config.add(configuration).create()
            success_messages.append(f"ETHERNET INTERFACE:{interface_config['name']} successfully configured."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: ETHERNET INTERFACE:{interface_config['name']} failed to configure with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages


def l3sub_interface_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for int_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{int_config['template']}")
        ## extract the parent interface
        parent_interface = int_config["name"].split(".")[0]
        # print(parent_interface)
        interface_parent = AggregateInterface(f"{parent_interface}")
        # pop the template name to create a dictionary of layer3 sub interface configuration
        int_config.pop("template")
        # Generate configuration
        configuration = Layer3Subinterface(**int_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter parent interface configuration
            interface_config = template_config.add(interface_parent)
            # configure the L3 sub interface
            interface_config.add(configuration).create()
            success_messages.append(f"SUB-INTERFACE:{int_config['name']} successfully configured."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: SUB-INTERFACE:{int_config['name']} failed to configure with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages

def loopback_interface_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for interface_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{interface_config['template']}")
        # pop the template name to create a dictionary of loopback interface configuration
        interface_config.pop("template")
        # Generate configuration
        configuration = LoopbackInterface(**interface_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            template_config.add(configuration).create()
            success_messages.append(f"LOOPBACK INTERFACE:{interface_config['name']} successfully configured."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: LOOPBACK INTERFACE:{interface_config['name']} failed to configure with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages

def tunnel_interface_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for interface_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{interface_config['template']}")
        # pop the template name to create a dictionary of tunnel interface configuration
        interface_config.pop("template")
        # define configuration
        configuration = TunnelInterface(**interface_config)
        try:
            template_config = pano.add(template_parent)
            template_config.add(configuration).create()
            success_messages.append(f"TUNNEL INTERFACE:{interface_config['name']}successfully configured."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: TUNNEL INTERFACE:{interface_config['name']} failed to configure with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages

def vr_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for vr_config in track(config_facts):
        # # define configuration tree
        template_parent = Template(f"{vr_config['template']}")
        # pop the template name to create a dictionary of vsys configuration
        vr_config.pop("template")
        # Generate virtual router configuration
        configuration = VirtualRouter(**vr_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            template_config.add(configuration).create()
            success_messages.append(f"VIRTUAL ROUTER:{vr_config['name']} successfully configured."
            )
        # exception message of virtual router failed to create
        except Exception as msg:
            failure_messages.append(
                f"Failed: VIRTUAL ROUTER:{vr_config['name']} failed to configure with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages

def zone_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for zone_config in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{zone_config['template']}")
        vsys_parent = Vsys(f"{zone_config['vsys']}")
        # pop template and vsys names to create a dictionary of vsys configuration
        zone_config.pop("template")
        zone_config.pop("vsys")
        # define configuration
        configuration = Zone(**zone_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            vsys_config = template_config.add(vsys_parent)
            # configure zone
            vsys_config.add(configuration).create()
            success_messages.append(f"ZONE:{zone_config['name']} successfully configured in VSYS:{vsys_parent}."
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: ZONE:{zone_config['name']} failed to configure in VSYS:{vsys_parent} with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages

def static_route_configuration(config_facts, logfile, pano) -> str:
    success_messages = []
    failure_messages = []
    for route_configuration in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{route_configuration['template']}")
        virtual_router_parent = VirtualRouter(
            f"{route_configuration['virtual_router']}"
        )
        # pop template and virtual router configuration to create a dictionary of static route configuration
        route_configuration.pop("template")
        route_configuration.pop("virtual_router")
        # define configuration
        configuration = StaticRoute(**route_configuration)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # configure zone
            virtual_router_config.add(configuration).create()
            success_messages.append(f"STATIC ROUTE:{route_configuration['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}"
            )
        except Exception as msg:
            failure_messages.append(
                f"Failed: STATIC ROUTE:{route_configuration['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}\n"
            )

    # return the success and failure messages
    return success_messages, failure_messages