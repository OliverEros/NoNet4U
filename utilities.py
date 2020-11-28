from subprocess import PIPE, call, check_output
import netifaces
import re

from getmac import get_mac_address


"""
[NETIFACE UTILITIES] - GETTING INTERFCE, MAC, IP, ETC.
"""

def get_interface():
    gate = netifaces.gateways()
    if 'default' in gate and netifaces.AF_INET in gate['default']:
            return gate['default'][netifaces.AF_INET][1]

def get_gateway():
    gate = netifaces.gateways()
    if 'default' in gate and netifaces.AF_INET in gate['default']:
            return gate['default'][netifaces.AF_INET][0]

def get_netmask(interface):
    netmask = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in netmask:
        return netmask[netifaces.AF_INET][0]['netmask']

def get_interface_MAC(interface):
    mac = netifaces.ifaddresses(interface)
    if netifaces.AF_LINK in mac:
        return mac[netifaces.AF_LINK][0]['addr']

def get_user_MAC(host_ip):
   return get_mac_address(ip= host_ip)

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
    
    TO SOLVE:
    [*] Create a parser which accepts a string containing number + unit (e.g. 1mbps )
    [*] Parse and extract the number and unit
    [*] Convert the number to bare number (bit) based on the unit
              
"""
  
def cust_unit_to_barebits(rate):
    _rate = [x for x in rate]

    speed_nums = []
    unit_chars = []


    for char in _rate:
        if char.isnumeric():
            speed_nums.append(char)
        else:
            unit_chars.append(char)

    speed = ''.join(str(n) for n in speed_nums )
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
         raise Exception('Invalid unit')







