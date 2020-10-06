from random import randint


class MemBlock:

    def __init__(self, addr):
        self.addr = addr
        self.data = hex(randint(0, 2**16))

    def __str__(self):
        return self.addr + "|" + str(self.data)