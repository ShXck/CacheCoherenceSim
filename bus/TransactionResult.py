
class TransactionResult:

    def __init__(self, receiver, data, tag=None, addr=None):
        self.receiver = receiver
        self.data = data
        self.tag = tag
        self.addr = addr