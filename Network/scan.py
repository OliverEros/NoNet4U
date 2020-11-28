import socket
from scapy.all import ARP, sr1, Ether, conf
from Network.user import User
from ipaddress import IPv4Address
from netaddr import IPNetwork
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


class Scan:
    def __init__(self, netiface, iprange):
        self.netiface = netiface
        self.ip_range = iprange

        self.threads = 75

    def scan_for_hosts(self):

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            hosts = []
            address_range = [str(address)
                             for address in IPNetwork(self.ip_range)]
            """ Progress bar tqdm"""
            addresses_to_ARP = list(tqdm(executor.map(self.send_ARP, address_range), total=len(address_range))) 

            for host in addresses_to_ARP:
                if host is not None:
                    try:
                        host_details = socket.gethostbyaddr(host.ip)
                        host.name = '' if host_details is None else host_details[0]
                        hosts.append(host)
                    except socket.herror:
                        pass
            return hosts

    def send_ARP(self, ip):
        arp_packet = ARP(pdst=ip)
        result = sr1(arp_packet, retry=0, iface=self.netiface,
                     timeout=2, verbose=0)

        if result is not None:
            return User(ip, result.hwsrc, '')
