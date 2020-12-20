import socket
from scapy.all import ARP, sr1, Ether, conf
from Network.user import User
from ipaddress import IPv4Address
from netaddr import IPNetwork
from concurrent.futures import ThreadPoolExecutor


from tqdm import tqdm
import click



class Scan:
    def __init__(self, netiface, iprange,own_MAC):
        self.netiface = netiface
        self.ip_range = iprange
        self.own_MAC = own_MAC


        self.threads = 75

    """
    Using threading, ARP packets are sent to all available users in the subnet 
    For future: allows users to define their given range (self.ip_range if iprange == None else iprange)
    """
    def scan_for_hosts(self, iprange = None):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            hosts = []
            address_range = [str(address)
                             for address in IPNetwork(self.ip_range if iprange == None else iprange)]
            """ Progress bar tqdm"""
            addresses_to_ARP = list(tqdm(executor.map(self.send_ARP, address_range), total=len(address_range))) 

            """
            _host_id -> Assign ID to the user which can be used as a reference to limit,block, or free a given user

            """
            _host_id = 0
            for host in addresses_to_ARP:
                if host is not None:
                    try:
                        # Get mac of each device on the network
                        host.host_id = _host_id 
                        host_details = socket.gethostbyaddr(host.ip) # Get host details using the socket packet
                        host.name = '' if host_details is None else host_details[0]
                        hosts.append(host)
                        _host_id += 1 
                    except socket.herror:
                        pass
            return hosts

    """
    Sends ARP packets to the client for discovery reasons
    """
    def send_ARP(self, ip):
        arp_packet = ARP(pdst=ip)
        result = sr1(arp_packet, retry=0, iface=self.netiface,
                     timeout=2, verbose=0)

        if result is not None:
            return User(ip, result.hwsrc, '')



