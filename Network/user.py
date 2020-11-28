class User:
    def __init__(self, ip, mac, name):
        self.ip = ip
        self.mac = mac
        self.name = name
        self.isLimited = False
        self.isBlocked = False
        self.isSpoofed = False

  
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return self.__str__