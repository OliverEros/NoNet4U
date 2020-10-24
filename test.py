from Network.user import User
from Network.scan import Scan
from utilities import get_interface, get_gateway, get_netmask
from ipaddress import IPv4Address
from netaddr import IPNetwork


interface = get_interface()
gateway = get_gateway()
netmask = get_netmask(interface)


print('Interface : ' + interface)
print('Gateway : ' + gateway)
print('Netmask : ' + netmask)

scan = Scan(interface, gateway + '/' + netmask).scan_for_hosts()


