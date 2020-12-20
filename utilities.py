from subprocess import PIPE, call, check_output
import netifaces
import re
import click
import os

from getmac import get_mac_address


"""
[NETIFACE UTILITIES] - GETTING INTERFCE, MAC, IP, ETC.
"""

def get_interface():
    gate = netifaces.gateways()
    if 'default' in gate and netifaces.AF_INET in gate['default']:
            return gate['default'][netifaces.AF_INET][1]
    else:
        return False
    
        
def get_gateway():
    gate = netifaces.gateways()
    if 'default' in gate and netifaces.AF_INET in gate['default']:
            return gate['default'][netifaces.AF_INET][0]
    else:
        return False
    

def get_netmask(interface):
    netmask = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in netmask:
        return netmask[netifaces.AF_INET][0]['netmask']
    else:
        return False

def get_interface_MAC(interface):
    mac = netifaces.ifaddresses(interface)
    if netifaces.AF_LINK in mac:
        return mac[netifaces.AF_LINK][0]['addr']
    else:
        return False

def get_user_MAC(host_ip):
   return str(get_mac_address(ip= host_ip))


#IP FORWARDING FOR ARP - MAKES THE COMPUTER ACT AS A ROUTER
def enable_IP_forwarding():
    cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

def disable_IP_forwarding():
    cmd('echo 0 > /proc/sys/net/ipv4/ip_forward')

"""
[COMMAND LINE UTILITIES] - EXECUTING SHELL COMMANDS
"""

def cmd( command,root = True):
    call('sudo ' + command if root else command, shell=True)
   





"""
 [INPUT HANDLER ]

    [*] tc can set the allowed to rate to kbit, mbit, gbit, bps, etc.
    [*] Invoked in the modue Network.limit 
    [*] Function limit calculated the burst from the rate argument, which is a string
    [*] Therefore, it can't contain non-numeric values, only numbers
    [*] Based on the Linux manual page:
        [*] These parameters accept a floating point number, possibly followed by either a unit or a float
        [*] If specifying by bits :   bit or a BARE NUMBER
              
"""


def check_if_root():
    return os.getuid 

  
def cust_unit_to_barebits(rate):
    _rate = [x for x in rate]

    speed_nums = []
    unit_chars = []


    for char in _rate:
        if char.isnumeric():
            speed_nums.append(char)
        else:
            unit_chars.append(char)

    speed = int(''.join(str(n) for n in speed_nums ))
    unit = ''.join(unit_chars).lower()

    """
    Converts speed to bits based on the unit

    1 kb = 1024 bits
    1 mb = 1024 kb (1024 * 1024)
    1 gb = 1204 mb (1024 * 1024 * 1024)
    """

    if unit == 'kb':
        return speed
    elif unit == 'mb':
        return speed * 1024 ** 2
    elif unit == 'gb': 
        return speed * 1024 ** 3
    else:
         raise click.BadParameter('Invalid unit!')

def create_qdics(interface):
    cmd('/sbin/tc qdisc add dev {} root handle 1:0 htb'.format(interface))

def delete_qdisc(interface):
    cmd('/sbin/tc qdisc del dev {} root handle 1:0 htb'.format(interface))

def complete_iptables_reset():
    cmd('/sbin/iptables --policy INPUT ACCEPT')
    cmd('/sbin/iptables --policy OUTPUT ACCEPT')
    cmd('/usr/sbin/iptables --policy FORWARD ACCEPT')

    cmd('/sbin/iptables -Z')
    cmd('/sbin/iptables -F')
    cmd('/sbin/iptables -X')
