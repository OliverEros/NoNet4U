import netifaces


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

        
    


    
