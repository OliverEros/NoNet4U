from Network.user import User
import os
import threading

from utilities import cmd


class Limiter:
    def __init__(self, interface):
        self.interface = interface

        self.download = 1
        self.upload = 2
        self._block = 3

    """
    Create a unique ID for the user that can be used for TC
    """

    def _id_for_host(self, hosts):

        def _create_id(*id):
            
            _id = 1
            while True:
                if _id not in id:
                    values = (x for x in hosts.values())

                    _download_ids = (x['download_id'] for x in values)
                    _upload_ids = (x['upload_id'] for x in values)

                    _all_ids = set(_download_ids).union(set(_upload_ids))

                    if _id not in _all_ids:
                        return _id
                
                _id += 1

    
        id = _create_id()
        return id, _create_id(id)

        

    def limit(self, host, dw_up, rate, hosts):
        host_ids = self._id_for_host(hosts)
        down_or_up = None

        if dw_up == self.download:
            down_or_up = 1
            print(host_ids[0])

            """Create tc class"""
            cmd('/sbin/tc class add dev {} parent 1:0 classid 1:{} htb rate {r} burst {b}'.format(self.interface, host_ids[0],r = rate, b = rate * 1.1))
            """Mark flow"""
            cmd('/sbin/tc filter add dev {} protocol ip parent 1:0 prio {id} handle {id} fw flowid 1:{id}'.format(self.interface, id=host_ids[0]))
            """Iptable"""
            cmd('/sbin/iptables -t mangle -A POSTROUTING -d {} -j MARK --set-mark {} '.format(host.ip, host_ids[0]))
        if dw_up == self.upload:
            down_or_up = 2

            cmd('/sbin/tc class add dev {} parent 1:0 classid 1:{} htb rate {r} burst {b}'.format(self.interface, host_ids[1], r = rate, b = rate * 1.1 ))
            """Mark flow"""
            cmd('/sbin/tc filter add dev {} protocol ip parent 1:0 prio {id} handle {id} fw flowid 1:{id}'.format(self.interface, id=host_ids[0]))
            """Iptable"""
            cmd('/sbin/iptables -t mangle -A PREROUTING -s {} -j MARK --set-mark {} '.format(host.ip, host_ids[0]))

        host.isLimited = True
        hosts[host] =  {"download_id": host_ids[0], "upload_id": host_ids[1], "rate": rate, "up_or_down": down_or_up}
        
        
    """
    Unlimit user by deleting both the TC class and IP rules
    """
    def unlimit(self, host, hosts):
        if not host.isLimited and not host.isBlocked:
            return
        self.remove_tc_class(self.interface,host,hosts)
        self.remove_user_iptables(host,hosts)

        host.isLimited = False
        host.isBlocked = False
        hosts.pop(host)
        
       
    """
    Block user by dropping all packets to the given address (incoming and outgoing)
    """

    def block(self, host,hosts):
        
        cmd('/sbin/iptables -A  FORWARD -s {} -j DROP'.format(host.ip))
        cmd('/sbin/iptables -A  FORWARD -d {} -j DROP'.format(host.ip))

        host.isBlocked = True
        hosts[host] = {"download_id": None, "upload_id": None, "rate": None, "up_or_down": 3}
    
    def remove_tc_class(self, interface, host,hosts):
        if hosts[host]['up_or_down'] == 1:
            cmd('/sbin/tc filter delete dev {} prio {}'.format(interface, hosts[host]['download_id']))
            cmd('/sbin/tc class delete dev {} parent 1:0 classid 1:{}'.format(interface,hosts[host]['download_id']))
        elif hosts[host]['up_or_down'] == 2:
             cmd('/sbin/tc filter delete dev {} prio {}'.format(interface, hosts[host]['upload_id']))
             cmd('/sbin/tc class delete dev {} parent 1:0 classid 1:{}'.format(interface,hosts[host]['upload_id']))
        else:
            pass

    def remove_user_iptables(self, host, hosts):
        upload_id = hosts[host]['upload_id']
        download_id = hosts[host]['download_id']
        dw_or_up = hosts[host]['up_or_down']

        if dw_or_up == self.download:
            cmd('/sbin/iptables -t mangle -D POSTROUTING -d {} -j MARK --set-mark {}'.format(host.ip, download_id))
        if dw_or_up == self.upload:
            cmd('/sbin/iptables -t mangle -D PREROUTING -s {} -j MARK --set-mark {}'.format(host.ip, upload_id))
        if dw_or_up == self.block:
            cmd('/sbin/iptables -D  FORWARD -s {} -j DROP'.format(host.ip))
            cmd('/sbin/iptables -D  FORWARD -d {} -j DROP'.format(host.ip))


    @staticmethod
    def get_rate_input(rate):
        return rate

    
   

  



 
    

        
    
        

    

    
        

       


    



        
