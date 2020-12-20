

from Network.user import User
from Network.scan import Scan
from Network.ARP_spoofing import ARP_spoofer
from Network.limit import Limiter
from CLI.menu import main_menu
from CLI.logo import NONET4U_logo
from CLI.click_output import error_out, message_out
import click

from utilities import get_interface, get_gateway, get_netmask, get_interface_MAC, get_user_MAC, cust_unit_to_barebits, cmd, check_if_root, enable_IP_forwarding, create_qdics, delete_qdisc, complete_iptables_reset


from ipaddress import IPv4Address, ip_network
from netaddr import IPNetwork


def main():

    interface = get_interface()
    gateway = get_gateway()
    ip_range = gateway + '/' + str(get_netmask(interface))

    is_root = False

    if not check_if_root():
        error_out('You must run as root!')
        return False
    else:
        is_root = True

    if not interface:
        error_out('Interface could not be loaded')
        return
    elif not gateway:
        error_out('Gateway could not be loaded')
        return
    elif enable_IP_forwarding() == False:
        error_out('IP Forwarding could not be enabled!')
    else:

        delete_qdisc(interface)
        create_qdics(interface)
        complete_iptables_reset()

        arguments = [interface, gateway, ip_range]

        message_out(NONET4U_logo)
        error_out('Interface: ' + interface)
        error_out('Gateway: ' + gateway + '\n')
        
        menu = main_menu(arguments)

if __name__ == "__main__":
    main()
