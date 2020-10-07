from threading import Lock

from bus.Transaction import BusTransaction
from bus.TransactionResult import TransactionResult
from cache.Cache import L1Cache
from coherence.SnoopingController import SnoopingController
from processor.InstructionGenerator import InstructionGenerator
from cache.Enums import Instructions, BlockStates, TransactionState
import time


class Processor:

    def __init__(self, id, mainAddresses, lock):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)
        self.snoopingController = SnoopingController()
        self.lock = lock

    def startProcessor(self, bus):
        while True:
            # check bus here

            self.lock.acquire()
            try:
                print("P" + str(self.id) + " Acquired lock")
                self.checkTransactionResult(bus.transactionResult)
                print("P" + str(self.id) + " checks bus: " + str(bus.currentTransaction))
                self.handleBusTransaction(bus)

                currentInstr = self.instrGen.generateInstruction(self.id)
                print("P" + str(self.id) + " issued instruction: " + currentInstr)
                self.handleInstruction(currentInstr, bus)
            finally:
                print("P" + str(self.id) + " released lock")
                self.lock.release()

            time.sleep(1)

    def handleInstruction(self, instr, bus):
        '''
        Reads an instruction and do the operations needed to execute it.
        :param instr: Instruction issued by the processor.
        :param bus: Shared bus among processors.
        '''
        splitInstr = instr.split(" ")
        if splitInstr[1] == Instructions.READ.value:
            if not self.l1Cache.readValue(splitInstr[2]):
                print("Read miss")
                busTrans = BusTransaction(self.id, instr)

                if not bus.isBusy:
                    bus.addTransaction(busTrans)

                # TODO: generate alert

        elif splitInstr[1] == Instructions.WRITE.value:
            self.l1Cache.writeValue(splitInstr[2], splitInstr[3])


    def handleBusTransaction(self, bus):
        transaction = bus.currentTransaction

        if transaction is not None and transaction.state.value == TransactionState.UNRESOLVED.value and transaction.sender != self.id:
            print("P" + str(self.id) + " Transaction found: " + str(transaction))
            instr = transaction.instruction.split(" ")
            tag, index, offset = self.l1Cache.controller.processAddress(instr[2])

            ret, block = self.l1Cache.isInCache(tag)

            if ret and block.state != BlockStates.INVALID:
                # TODO: Update to other states
                bus.transactionResult = TransactionResult(transaction.sender, block.data, tag=tag)
                transaction.state = TransactionState.RESOLVED

            bus.updateTransaction()

    def checkTransactionResult(self, result):
        if result is not None:
            print("P" + str(self.id) + " CHECKING TRANSACTION " + str(result.receiver))
        '''
        Checks the transaction result that's on the bus to see if it's aimed at this processor.
        :param result: Transaction result.
        '''
        if result is not None and result.receiver == self.id:
            print("P" + str(self.id) + " is checking the result")
            for block in self.l1Cache.sets:
                # Check of result comes from main memory
                if result.tag is None:
                    # map the address to a block of cache
                    blockIndex, tag, index = self.l1Cache.controller.mapAddress(result.addr)
                    # sets the block data
                    block = self.l1Cache.sets[index].blocks[blockIndex]
                    # sets block new data
                    block.data = result.data
                    # sets block new tag
                    block.currentTag = tag
                # Data comes from another cache
                else:
                    if block.currenTag == result.tag:
                        block.data = result.data
                        block.state = BlockStates.SHARED



