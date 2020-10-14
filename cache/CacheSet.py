from random import randint

from cache import CacheBlock as block


class CacheSet:

    def __init__(self, blocks_qty):
        self.blocks = []

        blockId = 0

        for _ in range(blocks_qty):
            self.blocks.append(block.CacheBlock(blockId))
            blockId += 1

    def getBlockValue(self, tag):
        '''
        Retrieves the data value of a block, given the tag.
        :param tag: tag of the block.
        :return: data value.
        '''
        for block in self.blocks:
            if block.currentTag == tag:
                return block.data


    def getReplacementBlock(self):
        '''
        Checks which is the block least recently used to be replaced.
        :return: the block to be replaced.
        '''
        for block in self.blocks:
            if block.LRU == 1:
                return block

        return self.blocks[randint(0, 1)]




