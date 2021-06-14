import panos.panorama
import json
import yaml

from rich.console import Console
console = Console()

from utils.xls_to_facts import read_design
from utils.connect import panorama_connect
from utils.log import log_messages
from config_modules.panorama_tab import template_configuration
from config_modules.device_tab import vsys_configuration
from config_modules.network_tab import vr_configuration
from config_modules.network_tab import zone_configuration
from config_modules.network_tab import aggregate_interface_configuration
from config_modules.network_tab import ethernet_interface_configuration
from config_modules.network_tab import l3sub_interface_configuration
from config_modules.network_tab import loopback_interface_configuration
from config_modules.network_tab import tunnel_interface_configuration
from config_modules.network_tab import management_profile_configuration
from config_modules.network_tab import static_route_configuration

from panos.device import Vsys


def main():
    # initiate inventory file
    with open("inventory.yaml", "r") as file:
        try:
            inventory = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            console.print(f":thumbs_down: Unable to read inventory file: {exc}", style="bold red")
            exit(1)

    # print (inventory)
    # Open logfile
    logfile = open("logfile.log", "w")

    # invoke function to read the design file and convert to json
    design = read_design(inventory["data"]["design_file"], logfile)
    # print(json.dumps(design, indent=4))

    # invoke function to establish connection to panorama
    pano = panorama_connect(
        logfile,
        inventory["device_details"]["device_ip"],
        inventory["device_details"]["username"],
        inventory["device_details"]["password"],
    )

    # invoke function to configure template if in design facts
    if 'template' in design["facts"]:
        template_facts = design["facts"]["template"]
        console.print("\n[bold cyan]<-----CONFIGURING TEMPLATES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING TEMPLATES----->\n")
        success_messages, failure_messages = template_configuration(template_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure Management Profile if in design facts
    if 'management_profile' in design['facts']:
        profile_facts = design['facts']['management_profile']
        console.print("\n[bold cyan]<-----CONFIGURING MANAGEMENT PROFILE----->[/bold cyan]")
        logfile.write("<-----CONFIGURING MANAGEMENT PROFILE----->\n")
        success_messages, failure_messages = management_profile_configuration(profile_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure aggregate interfaces if in design facts
    if 'aggregate_interfaces' in design['facts']:
        agg_interface_facts = design['facts']['aggregate_interfaces']
        console.print("\n[bold cyan]<-----CONFIGURING AGGREGATE INTERFACES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING AGGREGATE INTERFACES----->\n")
        success_messages, failure_messages = aggregate_interface_configuration(agg_interface_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure ethernet interfaces if in design facts
    if 'ethernet_interfaces' in design['facts']:
        ethernet_interface_facts = design['facts']['ethernet_interfaces']
        console.print("\n[bold cyan]<-----CONFIGURING ETHERNET INTERFACES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING ETHERNET INTERFACES----->\n")
        success_messages, failure_messages = ethernet_interface_configuration(ethernet_interface_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure sub-interfaces if in design facts
    if 'sub_interfaces' in design['facts']:
        l3sub_interface_facts = design['facts']['sub_interfaces']
        console.print("\n[bold cyan]<-----CONFIGURING SUB-INTERFACES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING SUB-INTERFACES----->\n")
        success_messages, failure_messages = l3sub_interface_configuration(l3sub_interface_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure loopback interface if in design facts
    if 'loopback_interfaces' in design['facts']:
        loopback_interface_facts = design['facts']['loopback_interfaces']
        console.print("\n[bold cyan]<-----CONFIGURING LOOPBACK INTERFACES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING LOOPBACK INTERFACES----->\n")
        success_messages, failure_messages = loopback_interface_configuration(loopback_interface_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure tunnel interface if in design facts
    if 'tunnel_interfaces' in design['facts']:
        tunnel_interface_facts = design['facts']['tunnel_interfaces']
        console.print("\n[bold cyan]<-----CONFIGURING TUNNEL INTERFACES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING TUNNEL INTERFACES----->\n")
        success_messages, failure_messages = tunnel_interface_configuration(tunnel_interface_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure virtual routers if in design facts
    if 'virtual_router' in design['facts']:
        vr_facts = design['facts']['virtual_router']
        console.print("\n[bold cyan]<-----CONFIGURING VIRTUAL ROUTERS----->[/bold cyan]")
        logfile.write("<-----CONFIGURING VIRTUAL ROUTERS----->\n")
        success_messages, failure_messages = vr_configuration(vr_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # ! Deletes vsys1 (default vsys)
    # invoke function to configure vsys if in design facts
    if 'vsys' in design['facts']:
        vsys_facts = design['facts']['vsys']
        console.print("\n[bold cyan]<-----CONFIGURING VIRTUAL SYSTEMS----->[/bold cyan]")
        logfile.write("<-----CONFIGURING VIRTUAL SYSTEMS----->\n")
        success_messages, failure_messages = vsys_configuration(vsys_facts, template_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)

    # invoke function to configure zones if in desing facts
    if 'zone' in design['facts']:
        zone_facts = design['facts']['zone']
        console.print("\n[bold cyan]<-----CONFIGURING ZONES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING ZONES----->\n")
        success_messages, failure_messages = zone_configuration(zone_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)
    
    # invoke function to configure static routes if in design facts
    if 'static_routes' in design['facts']:
        static_route_facts = design['facts']['static_routes']
        console.print("\n[bold cyan]<-----CONFIGURING STATIC ROUTES----->[/bold cyan]")
        logfile.write("<-----CONFIGURING STATIC ROUTES----->\n")
        success_messages, failure_messages = static_route_configuration(static_route_facts, logfile, pano)
        log_messages(success_messages, failure_messages, logfile)


if __name__ == "__main__":
    main()
