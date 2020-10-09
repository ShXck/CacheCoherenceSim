from cache.Enums import TransactionState


class TransactionResponse:

    def __init__(self, addr):
        self.addr = addr
        self.data = None
        self.state = TransactionState.UNRESOLVED
        self.fromMemory = None
        self.read = False

    def __str__(self):
        return self.addr + "|" + str(self.data) + "|" + str(self.state) + "|" + str(self.fromMemory)

    def __eq__(self, other):
        if not isinstance(other, TransactionResponse):
            return False
        else:
            return self.addr == other.addr and self.data == other.data and self.state.value == other.state.value \
                   and self.read == other.read and self.fromMemory == other.fromMemory

