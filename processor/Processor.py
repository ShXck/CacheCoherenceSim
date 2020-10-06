from bus.Transaction import BusTransaction
from cache.Cache import L1Cache
from processor.InstructionGenerator import InstructionGenerator
from cache.Enums import Instructions
import time
from threading import Lock


class Processor:

    def __init__(self, id, mainAddresses):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)

    def startProcessor(self, bus):
        while True:
            currentInstr = self.instrGen.generateInstruction(self.id)
            self.handleInstruction(currentInstr, bus)
            time.sleep(1)

    def handleInstruction(self, instr, bus):
        splitInstr = instr.split(" ")

        if splitInstr[1] == Instructions.READ.value:
            if not self.l1Cache.readValue(splitInstr[2]):
                busTrans = BusTransaction(self.id, instr)
                # TODO: Mutex bus


        elif splitInstr[1] == Instructions.WRITE.value:
            self.l1Cache.writeValue(splitInstr[2], splitInstr[3])




