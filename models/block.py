from datetime import datetime
from util import calculate_hash


class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = calculate_hash(self)


class BlockChain:
    def __init__(self):
        self.blocks = []

        first_block = Block(0, None, datetime.now(), "first block")
        self.blocks.append(first_block)

    def new_block(self, data):
        latest_block = self.blocks[-1]
        return Block(latest_block.index + 1, latest_block.hash, datetime.now(), data)

    def add_block(self, block: Block):
        self.blocks.append(block)

    def is_first_block_valid(self):
        first_block = self.blocks[0]

        if first_block.index != 0:
            return False

        if first_block.previous_hash is not None:
            return False

        if first_block.hash is None or calculate_hash(first_block) != first_block.hash:
            return False

        return True

    @staticmethod
    def is_valid_block(block: Block, previous_block: Block):
        if previous_block.index + 1 != block.index:
            return False

        if block.previous_hash is None or block.previous_hash != previous_block.hash:
            return False

        if block.hash is None or calculate_hash(block) != block.hash:
            return False

        return True

    def is_block_chain_valid(self):
        if not self.is_first_block_valid():
            return False

        for i in range(1, len(self.blocks)):
            previous_block = self.blocks[i - 1]
            block = self.blocks[i]
            if not self.is_valid_block(block, previous_block):
                return False

        return True

    def __str__(self):
        chain = ""
        for block in self.blocks:
            chain += "Block #" + str(block.index) + " [" + "\n\tindex: " + str(
                block.index) + "\n\tprevious hash: " + str(block.previous_hash) + "\n\ttimestamp: " + str(
                block.timestamp) + "\n\tdata: " + str(block.data) + "\n\thash: " + str(
                block.hash) + "\n]\n"
            chain += "\n"

        return chain
