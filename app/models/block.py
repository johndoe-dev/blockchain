from datetime import datetime
from app.util import calculate_hash


class BlockChainException(Exception):
    pass


class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = calculate_hash(self)

    def serialize(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "hash": self.hash
        }


class BlockChain:
    blocks = []

    def __init__(self, data=None):
        if data:
            self.init_first(data)

    @staticmethod
    def init_first(data):
        if BlockChain.blocks:
            raise BlockChainException("The block chain has already been initialized")

        first_block = Block(0, None, datetime.now(), data)

        BlockChain.blocks.append(first_block)

    @staticmethod
    def new_block(data):
        latest_block = BlockChain.blocks[-1]
        return Block(latest_block.index + 1, latest_block.hash, datetime.now(), data)

    @staticmethod
    def add_block(block: Block):
        BlockChain.blocks.append(block)

    @staticmethod
    def is_first_block_valid():
        first_block = BlockChain.blocks[0]

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

        for i in range(1, len(BlockChain.blocks)):
            previous_block = BlockChain.blocks[i - 1]
            block = BlockChain.blocks[i]
            if not self.is_valid_block(block, previous_block):
                return False

        return True

    def __str__(self):
        chain = ""
        for block in BlockChain.blocks:
            chain += "Block #" + str(block.index) + " [" + "\n\tindex: " + str(
                block.index) + "\n\tprevious hash: " + str(block.previous_hash) + "\n\ttimestamp: " + str(
                block.timestamp) + "\n\tdata: " + str(block.data) + "\n\thash: " + str(
                block.hash) + "\n]\n"
            chain += "\n"

        return chain

    @staticmethod
    def serialize():
        return [block.serialize() for block in BlockChain.blocks]
