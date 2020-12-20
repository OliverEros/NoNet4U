class User:
    def __init__(self, ip, mac, name):
        self.host_id = None
        self.ip = ip
        self.mac = mac
        self.name = name
        self.isLimited = False
        self.isBlocked = False
        self.isSpoofed = False


    
    def get_status(self):
        if self.isLimited:
            return 'limited'
        elif self.isBlocked:
            return 'blocked'
        else:
            return 'free'

  

    
    def __repr__(self):
        return self.name

    
