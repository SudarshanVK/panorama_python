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
from panos.network import Bgp
from panos.network import BgpAuthProfile
from panos.network import BgpPeerGroup
from panos.network import BgpPeer
from panos.network import IkeCryptoProfile

import json
from rich.console import Console
from rich.progress import track

console = Console()


def management_profile_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: MANAGEMENT PROFILE: {profile_configuration['name']} successfully configured."
            )
            logfile.write(
                f" Successful: MANAGEMENT PROFILE: {profile_configuration['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: MANAGEMENT PROFILE: {profile_configuration['name']} failed to configure with message {msg}\n"
            )
            logfile.write(
                f" Failed: MANAGEMENT PROFILE: {profile_configuration['name']} failed to configure with message {msg}.\n"
            )


def aggregate_interface_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: AGGREGATE INTERFACE: {interface_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: AGGREGATE INTERFACE: {interface_config['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: AGGREGATE INTERFACE: {interface_config['name']} failed to configure with message {msg}\n"
            )
            logfile.write(
                f" Failed: AGGREGATE INTERFACE: {interface_config['name']} failed to configure with message {msg}.\n"
            )


def ethernet_interface_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: ETHERNET INTERFACE: {interface_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: ETHERNET INTERFACE: {interface_config['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: ETHERNET INTERFACE: {interface_config['name']} failed to configure with message {msg}\n"
            )
            logfile.write(
                f" Failed: ETHERNET INTERFACE: {interface_config['name']} failed to configure with message {msg}.\n"
            )


def l3sub_interface_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: SUB-INTERFACE: {int_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: SUB-INTERFACE: {int_config['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: SUB-INTERFACE: {int_config['name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: SUB-INTERFACE: {int_config['name']} failed to configure with message {msg}.\n"
            )


def loopback_interface_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: LOOPBACK INTERFACE: {interface_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: LOOPBACK INTERFACE: {interface_config['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: LOOPBACK INTERFACE: {interface_config['name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: LOOPBACK INTERFACE: {interface_config['name']} failed to configure with message {msg}.\n"
            )


def tunnel_interface_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: TUNNEL INTERFACE: {interface_config['name']}successfully configured."
            )
            logfile.write(
                f" Successful: TUNNEL INTERFACE: {interface_config['name']}successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: TUNNEL INTERFACE: {interface_config['name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: TUNNEL INTERFACE: {interface_config['name']} failed to configure with message {msg}.\n"
            )


def vr_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: VIRTUAL ROUTER: {vr_config['name']} successfully configured."
            )
            logfile.write(
                f" Successful: VIRTUAL ROUTER: {vr_config['name']} successfully configured.\n"
            )
        # exception message of virtual router failed to create
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: VIRTUAL ROUTER: {vr_config['name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: VIRTUAL ROUTER: {vr_config['name']} failed to configure with message {msg}.\n"
            )


def zone_configuration(config_facts, logfile, pano) -> None:
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
            console.print(
                f"[bold green] :thumbs_up: ZONE: {zone_config['name']} successfully configured in VSYS:{vsys_parent}."
            )
            logfile.write(
                f" Successful: ZONE: {zone_config['name']} successfully configured in VSYS:{vsys_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: ZONE: {zone_config['name']} failed to configure in VSYS:{vsys_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: ZONE: {zone_config['name']} failed to configure in VSYS:{vsys_parent} with message {msg}.\n"
            )


def static_route_configuration(config_facts, logfile, pano) -> None:
    for route_configuration in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{route_configuration['template']}")
        virtual_router_parent = VirtualRouter(
            f"{route_configuration['virtual_router']}"
        )
        # pop template and virtual router configuration to create a dictionary of static route configuration
        route_configuration.pop("template")
        route_configuration.pop("virtual_router")
        # set nexthop to "none" if interface has been set but nexthop has not been set
        if "interface" in route_configuration:
            if "nexthop" not in route_configuration:
                route_configuration.update({"nexthop": "None"})
            if "nexthop_type" not in route_configuration:
                route_configuration.update({"nexthop_type": "None"})
        # define configuration
        configuration = StaticRoute(**route_configuration)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # configure zone
            virtual_router_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: STATIC ROUTE: {route_configuration['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}."
            )
            logfile.write(
                f" Successful: STATIC ROUTE: {route_configuration['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: STATIC ROUTE: {route_configuration['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: STATIC ROUTE: {route_configuration['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}.\n"
            )


def bgp_base_configuration(config_facts, logfile, pano) -> None:
    for bgp_config in track(config_facts):
        # print (bgp_config)
        # define configuration tree
        template_parent = Template(f"{bgp_config['template']}")
        virtual_router_parent = VirtualRouter(f"{bgp_config['virtual_router']}")
        # pop template and virtual router configuration to create a dictionary of static route configuration
        bgp_config.pop("template")
        bgp_config.pop("virtual_router")
        # print (bgp_config)
        # define configuration
        configuration = Bgp(**bgp_config)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # configure zone
            virtual_router_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: BGP successfully configured in VIRTUAL ROUTER:{virtual_router_parent}."
            )
            logfile.write(
                f" Successful: BGP successfully configured in VIRTUAL ROUTER:{virtual_router_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: BGP failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: BGP failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}.\n"
            )


def bgp_auth_profile_configuration(config_facts, logfile, pano) -> None:
    for auth_profile in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{auth_profile['template']}")
        virtual_router_parent = VirtualRouter(
            f"{auth_profile['virtual_router']}"
        )
        # pop template and virtual router configuration to create a dictionary of static route configuration
        auth_profile.pop("template")
        auth_profile.pop("virtual_router")
        # print (bgp_config)
        # define configuration
        configuration = BgpAuthProfile(**auth_profile)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # enter BGP configuration
            bgp_config = virtual_router_config.add(Bgp())
            # configure zone
            bgp_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: BGP AUTH PROFILE: {auth_profile['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}."
            )
            logfile.write(
                f" Successful: BGP AUTH PROFILE: {auth_profile['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: BGP AUTH PROFILE: {auth_profile['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: BGP AUTH PROFILE: {auth_profile['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}.\n"
            )


def bgp_peer_groups_configuration(config_facts, logfile, pano) -> None:
    for peer_group in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{peer_group['template']}")
        virtual_router_parent = VirtualRouter(f"{peer_group['virtual_router']}")
        # pop template and virtual router configuration to create a dictionary of static route configuration
        peer_group.pop("template")
        peer_group.pop("virtual_router")
        # print (bgp_config)
        # define configuration
        configuration = BgpPeerGroup(**peer_group)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # enter BGP configuration
            bgp_config = virtual_router_config.add(Bgp())
            bgp_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: BGP PEER GROUP: {peer_group['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}."
            )
            logfile.write(
                f" Successful: BGP PEER GROUP: {peer_group['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: BGP PEER GROUP: {peer_group['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: BGP PEER GROUP: {peer_group['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}.\n"
            )


def bgp_peer_configuration(config_facts, logfile, pano) -> None:
    for peer in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{peer['template']}")
        virtual_router_parent = VirtualRouter(f"{peer['virtual_router']}")
        peer_group_parent = BgpPeerGroup(f"{peer['peer_group']}")
        # pop template, virtual router and peer group configuration to create a dictionary of static route configuration
        peer.pop("template")
        peer.pop("virtual_router")
        peer.pop("peer_group")
        # print (bgp_config)
        # define configuration
        configuration = BgpPeer(**peer)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            # enter vsys configuration
            virtual_router_config = template_config.add(virtual_router_parent)
            # enter BGP configuration
            bgp_config = virtual_router_config.add(Bgp())
            # enter BGP peer group
            bgp_peer_config = bgp_config.add(peer_group_parent)
            # Apply the peer configuration
            bgp_peer_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: BGP PEER : {peer['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}."
            )
            logfile.write(
                f" Successful: BGP PEER : {peer['name']} successfully configured in VIRTUAL ROUTER:{virtual_router_parent}.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: BGP PEER : {peer['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}."
            )
            logfile.write(
                f" Failed: BGP PEER : {peer['name']} failed to configure in VIRTUAL ROUTER:{virtual_router_parent} with message {msg}.\n"
            )


def ike_crypto_profile_configuration(config_facts, logfile, pano) -> None:
    for profile in track(config_facts):
        # define configuration tree
        template_parent = Template(f"{profile['template']}")
        # pop template name to create a dictionary of the profile configuration
        profile.pop("template")
        configuration = IkeCryptoProfile(**profile)
        try:
            # Enter template configuration
            template_config = pano.add(template_parent)
            template_config.add(configuration).create()
            console.print(
                f"[bold green] :thumbs_up: IKE CRYPTO PROFILE : {profile['name']} successfully configured."
            )
            logfile.write(
                f" Successful: IKE CRYPTO PROFILE : {profile['name']} successfully configured.\n"
            )
        except Exception as msg:
            console.print(
                f"[bold red] :thumbs_down: IKE CRYPTO PROFILE : {profile['name']} failed to configure with message {msg}."
            )
            logfile.write(
                f" Failed: IKE CRYPTO PROFILE : {profile['name']} failed to configure with message {msg}.\n"
            )
