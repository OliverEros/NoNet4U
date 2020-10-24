class User:
    def __init__(self, ip, mac, name):
        self.ip = ip
        self.mac = mac
        self.name = name
        self.isLimited = False
        self.isBlocked = False

  
    def __str__(self):
        return str(self.ip)