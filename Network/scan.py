import socket
from scapy.all import ARP, sr1, Ether, conf
from Network.user import User
from Network.user import User
from ipaddress import IPv4Address
from netaddr import IPNetwork
from concurrent.futures import ThreadPoolExecutor


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
            addresses_to_ARP = executor.map(self.send_ARP, address_range)

            for host in addresses_to_ARP:
                if host is not None:
                    try:
                        host_details = socket.gethostbyaddr(host.ip)
                        host.name = '' if host_details is None else host_details[0]
                        hosts.append(host)
                    except socket.herror:
                        pass
            return hosts

            for address in IPNetwork(self.ip_range):
                user = self.send_ARP(str(address))
                if user is not None:
                    print(user)

    def send_ARP(self, ip):
        arp_packet = ARP(pdst=ip)
        result = sr1(arp_packet, retry=0, iface=self.netiface,
                     timeout=2, verbose=0)

        if result is not None:
            return User(ip, result.hwsrc, '')
