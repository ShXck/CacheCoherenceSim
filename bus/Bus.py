from bus.TransactionResult import TransactionResult
from cache.Enums import TransactionState

class Bus:

    def __init__(self, processors, memory):
        self.listeningProcessors = processors
        self.mainMem = memory
        self.currentTransaction = None
        self.isBusy = False
        self.transactionResult = None

    def addTransaction(self, transaction):
        '''
        Sets the current transaction of the bus.
        :param transaction: transaction to be processed.
        '''
        self.currentTransaction = transaction
        self.isBusy = True

    def updateTransaction(self):
        self.currentTransaction.accessCount += 1
        accesses = len(self.listeningProcessors) - 1

        if self.currentTransaction.accessCount == accesses and self.currentTransaction.state.value == TransactionState.UNRESOLVED.value:
            print("Gotta go to memory boy")
            # if no cache found the data, go for memory
            instr = self.currentTransaction.instruction.split(" ")
            memData = self.mainMem.getMemData(instr[2])
            print("Memory data: " + str(memData))
            self.transactionResult = TransactionResult(self.currentTransaction.sender, memData, addr=instr[2])
            self.currentTransaction.state = TransactionState.RESOLVED










