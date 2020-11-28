from Network.user import User
import os
import threading

from utilities import cmd


class Limiter:
    def __init__(self, interface):
        self.interface = interface
        self.hosts = {}

        self.download = 1
        self.upload = 2
        self._block = 3


    def _id_for_host(self, host):
        upload_id = 1
        download_id = 1

        for user in self.hosts:
            if set[user]['dw'] == download_id:
                download_id += 1
            if set[user]['up'] == upload_id:
                 upload_id += 1

        return download_id, upload_id

    def limit(self, host, dw_up, rate):
        host_ids = self._id_for_host(host)
        down_or_up = None

        if dw_up == self.download:
            down_or_up = 1

            """Create tc class"""
            cmd('/usr/sbin/tc class add dev {} parent 1:0 classid 1:{} htb rate {r} burst {b}'.format(self.interface, host_ids[0],r = rate * 1024 ** 2, b = rate * 1024 ** 2 * 1.1))
            """Mark flow"""
            cmd('/usr/sbin/tc filter add dev {} protocol ip parent 1:0 prio {id} handle {id} fw flowid 1:{id}'.format(self.interface, id=host_ids[0]))
            """Iptable"""
            cmd('/usr/sbin/iptables -t mangle -A POSTROUTING -d {} -j MARK --set-mark {} '.format(host.ip, host_ids[0]))
        if dw_up == self.upload:
            down_or_up = 2

            cmd('/usr/sbin/tc class add dev {} parent 1:0 classid 1:{} htb rate {r} burst {b}'.format(self.interface, host_ids[1], r = rate * 1024 ** 2, b = rate * 1.1 ))
            """Mark flow"""
            cmd('/usr/sbin/tc filter add dev {} protocol ip parent 1:0 prio {id} handle {id} fw flowid 1:{id}'.format(self.interface, id=host_ids[0]))
            """Iptable"""
            cmd('/usr/sbin/iptables -t mangle -A PREROUTING -s {} -j MARK --set-mark {} '.format(host.ip, host_ids[0]))

        host.isLimited = True
        self.hosts[host] = {"download_id": host_ids[0], "upload_id": host_ids[1], "rate": rate, "up_or_down": down_or_up}
        

    def unlimit(self, host):
        if not host.isLimited and not host.isBlocked:
            return

        self.remove_tc_class(self.interface,host)
        self.remove_iptable(host)

        self.hosts.pop(host)
        host.isLimited = False
       

    def block(self, host):
        
        cmd('/usr/sbin/iptables -A  FORWARD -s {} -j DROP'.format(host.ip))
        cmd('/usr/sbin/iptables -A  FORWARD -d {} -j DROP'.format(host.ip))

        self.hosts[host] = {"download_id": None, "upload_id": None, "rate": None, "up_or_down": 3}
    
    def remove_tc_class(self, interface, host):
            cmd('/usr/sbin/tc filter delete dev {} prio {}'.format(interface, download_id))
            cmd('/usr/sbin/tc class delete dev {} parent 1:0 classid 1:{}'.format(interface, download_id))

    def remove_user_iptables(self, host):
        upload_id = self.hosts[host]['upload_id']
        download_id = self.hosts[host]['download_id']
        dw_or_up = self.hosts[host]['up_or_down']

        if dw_or_up == self.download:
            cmd('/usr/sbin/iptables -t mangle -D POSTROUTING -d {} -j MARK --set-mark {}'.format(host.ip, download_id))
        if dw_or_up == self.upload:
            cmd('/usr/sbin/iptables -t mangle -D PREROUTING -s {} -j MARK --set-mark {}'.format(host.ip, upload_id))
        if dw_or_up_up == self.block:
            cmd('/usr/sbin/iptables -D  FORWARD -s {} -j DROP'.format(host.ip))
            cmd('/usr/sbin/iptables -D  FORWARD -d {} -j DROP'.format(host.ip))


    @staticmethod
    def get_rate_input(rate):
        return rate

    @staticmethod
    def complete_iptables_reset():
        cmd('/usr/sbin/iptables --policy INPUT ACCEPT')
        cmd('/usr/sbin/iptables --policy OUTPUT ACCEPT')
        cmd('/usr/sbin/iptables --policy FORWARD ACCEPT')

        cmd('/usr/sbin/iptables -Z')
        cmd('/usr/sbin/iptables -F')
        cmd('/usr/sbin/iptables -X')

    @staticmethod
    def create_qdics(interface):
        cmd('/usr/sbin/tc qdisc add dev {} root handle 1:0 htb'.format(interface))

    @staticmethod
    def delete_qdisc(interface):
        cmd('/usr/sbin/tc qdisc del dev {} root handle 1:0 htb'.format(interface))

 
    

        
    
        

    

    
        

       


    



        
