
class BusTransaction:

    def __init__(self, senderID, addr, type):
        self.sender = senderID
        self.addr = addr
        self.transType = type
        self.accessCount = 0


    def __str__(self):
        return "P" + str(self.sender) + "|" + self.addr + "|" + str(self.transType)

    def __eq__(self, other):
        if not isinstance(other, BusTransaction):
            return False
        else:
            return self.sender == other.sender and self.addr == other.addr and self.transType.value == other.transType.value
