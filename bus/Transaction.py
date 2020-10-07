from cache.Enums import TransactionState


class BusTransaction:

    def __init__(self, senderID, instr, receiver=None):
        self.sender = senderID
        self.instruction = instr
        self.receiver = receiver
        self.state = TransactionState.UNRESOLVED
        self.accessCount = 0



    def __str__(self):
        return str(self.sender) + "|" + self.instruction + "|" + str(self.accessCount)
