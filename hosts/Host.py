class Host:
    def __init__(self, ip, mac, name):
        self.ip = str(ip)
        self.mac = str(mac)
        self.name = str(name)
        self.on_use = False

    def setOnUse(value):
        self.on_use = value is True
