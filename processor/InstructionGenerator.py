from random import randint

from numpy import random
import numpy as np


class InstructionGenerator:

    def __init__(self, addresses):
        self.instructions = ["CALC", "READ", "WRITE"]
        self.addressesAvailable = addresses

    def generateInstruction(self, processorID):
        '''
        Generates a random instruction.
        :return: random instruction.
        '''

        addressRandom = random.binomial(n=10, p=0.0625, size=16)
        instrRandom = random.binomial(n=10, p=0.33, size=3)

        instr = self.instructions[int(np.argmax(instrRandom))]

        if instr == self.instructions[1]:
            return "P" + str(processorID) + " " + instr + " " + str(self.addressesAvailable[np.argmax(addressRandom)])
        elif instr == self.instructions[2]:
            return "P" + str(processorID) + " " + instr + " " + str(self.addressesAvailable[np.argmax(addressRandom)]) + " "\
                   + str(hex(randint(0, 2 ** 16)))
        else:
            return "P" + str(processorID) + " " + instr
