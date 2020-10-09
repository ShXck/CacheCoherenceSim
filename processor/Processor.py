from threading import Lock

from bus.Transaction import BusTransaction
from cache.Cache import L1Cache
from coherence.SnoopingController import SnoopingController
from processor.InstructionGenerator import InstructionGenerator
from cache.Enums import Instructions, BlockStates, TransactionState, TransactionType
import time


class Processor:

    def __init__(self, id, mainAddresses, lock):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)
        self.snoopingController = SnoopingController()
        self.lock = lock
        self.waiting = False

    def startProcessor(self, bus):
        while True:
            # check bus here
            self.snoop(bus)
            if not self.waiting:
                currentInstr = self.instrGen.generateInstruction(self.id)
                print("\nP" + str(self.id) + " issued instruction: " + currentInstr)
                self.handleInstruction(currentInstr, bus)

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
                # Read miss is detected, so halt the instruction generation until miss is resolved.
                self.waiting = True
                self.lock.acquire()
                # Creates the new transaction to send into the bus
                busTrans = BusTransaction(self.id, splitInstr[2], TransactionType.READ_MISS)
                # Sends transaction to the bus
                bus.addTransaction(busTrans)
                self.lock.release()

        elif splitInstr[1] == Instructions.WRITE.value:
            needTrans, transType = self.l1Cache.writeValue(splitInstr[2], splitInstr[3])
            if needTrans:
                busTrans = BusTransaction(self.id, splitInstr[2], transType)
                self.lock.acquire()
                bus.addTransaction(busTrans)
                self.lock.release()
                self.waiting = True

    def snoop(self, bus):
        '''
        Snoops on the bus to see if there are transactions that affects the processor.
        :param bus: common bus among processors and main memory.
        '''
        for i in range(0, len(bus.transactions) - 1):
            trans, resp = bus.transactions[i]
            print("\nP" + str(self.id) + " read: " + str(trans) + " and " + str(resp))
            # checks if it is a read miss that this processor issued
            if trans.transType.value == TransactionType.READ_MISS.value:
                # Process transaction result
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    # Update block that caused a READ MISS
                    self.l1Cache.updateBlock(resp)
                    resp.read = True
                    # Transaction is complete
                    self.lock.acquire()
                    bus.updateTransactions()
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                else:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID:
                        resp.data = block.data
                        resp.state = TransactionState.RESOLVED
                        resp.fromMem = False
                        block.state = BlockStates.SHARED

                    self.lock.acquire()
                    bus.updateTransaction(i)
                    self.lock.release()

            # Case of invalidation due to a modification in another cache
            elif trans.transType.value == TransactionType.INVALIDATE.value:
                if trans.sender != self.id:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)

                    if found:
                        # invalidates the block
                        block.state = BlockStates.INVALID

                    self.lock.acquire()
                    bus.updateTransaction(i)
                    bus.updateTransactions()
                    self.lock.release()

            elif trans.transType.value == TransactionType.WRITE_MISS.value:
                if trans.sender == self.id and resp.state.value == TransactionState.RESOLVED.value:
                    self.l1Cache.updateBlock(resp)
                    resp.read = True
                    # Transaction is complete
                    self.lock.acquire()
                    bus.updateTransactions()
                    self.lock.release()
                    # Processor can keep on generating instructions
                    self.waiting = False
                else:
                    found, block = self.l1Cache.getCacheBlock(trans.addr)
                    if found and block.state.value != BlockStates.INVALID:
                        resp.data = block.data
                        resp.state = TransactionState.RESOLVED
                        resp.fromMem = False
                        block.state = BlockStates.SHARED

                    self.lock.acquire()
                    bus.updateTransaction(i)
                    self.lock.release()















