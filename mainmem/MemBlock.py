from random import randint


class MemBlock:

    def __init__(self, addr):
        self.addr = addr.zfill(4)
        self.data = hex(0)

    def __str__(self):
        return self.addr + "|" + str(self.data)