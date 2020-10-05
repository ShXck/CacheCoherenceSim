from cache.Cache import L1Cache
from processor.InstructionGenerator import InstructionGenerator
import time


class Processor:

    def __init__(self, id, mainAddresses):
        self.id = id
        self.l1Cache = L1Cache(4, 4, 2, 2)
        self.instrGen = InstructionGenerator(mainAddresses)

    def startProcessor(self, bus):
        while True:
            print(self.instrGen.generateInstruction(self.id))
            time.sleep(1)



