from cache.Enums import TransactionState


class TransactionResponse:

    def __init__(self, addr):
        self.addr = addr
        self.data = None
        self.state = TransactionState.UNRESOLVED
        self.fromMemory = None
        self.read = False

    def updateResponse(self, data, fromMem):
        '''
        Updates values and state of the transaction response
        :param data: data of the response.
        :param fromMem: whether or not value came from memory.
        '''
        self.data = data
        self.fromMemory = fromMem
        self.state = TransactionState.RESOLVED

    def __str__(self):
        return self.addr + "|" + str(self.data) + "|" + str(self.state) + "|" + str(self.fromMemory)

    def __eq__(self, other):
        if not isinstance(other, TransactionResponse):
            return False
        else:
            return self.addr == other.addr and self.data == other.data and self.state.value == other.state.value \
                   and self.read == other.read and self.fromMemory == other.fromMemory

