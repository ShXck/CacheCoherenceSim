from cache import CacheBlock as block


class CacheSet:

    def __init__(self, blocks_qty):
        self.blocks = []

        blockId = 0

        for _ in range(blocks_qty):
            self.blocks.append(block.CacheBlock(blockId))
            blockId += 1


