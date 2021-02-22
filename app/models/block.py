from typing import List
from datetime import datetime
from app.util import calculate_hash
from app.models.blockchain_exception import (
    BlockChainAlreadyInitError,
    BlockChainNotInitializedError,
    BlockChainDataInvalid,
    BlockChainInvalid,
    BlockChainInvalidList)


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        if hash:
            self.hash = hash
        else:
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
            raise BlockChainAlreadyInitError

        if not data:
            raise BlockChainDataInvalid

        first_block = Block(0, None, datetime.now(), data)

        BlockChain.blocks.append(first_block)

    @staticmethod
    def new_block(data):
        if not BlockChain.blocks:
            raise BlockChainNotInitializedError

        if not data:
            raise BlockChainDataInvalid

        latest_block = BlockChain.blocks[-1]
        return Block(latest_block.index + 1, latest_block.hash, datetime.now(), data)

    @staticmethod
    def add_block(block: Block):
        BlockChain.blocks.append(block)

    def init_from_list_of_dict(self, _list: List[dict]):

        try:
            sorted_list = sorted(_list, key=lambda key: key['index'])
            BlockChain.blocks = [Block(**data) for data in sorted_list]
        except TypeError:
            raise BlockChainInvalidList
        except KeyError:
            raise BlockChainInvalidList
        print(BlockChain.serialize())

        if not self.is_block_chain_valid(False):
            raise BlockChainInvalid

    @staticmethod
    def is_first_block_valid(check_hash=True):
        if not BlockChain.blocks:
            return True

        first_block = BlockChain.blocks[0]

        if first_block.index != 0:
            print("first block index not 0")
            return False

        if first_block.previous_hash is not None:
            print("first block previous_hash not None")
            return False

        if check_hash:
            if first_block.hash is None or calculate_hash(first_block) != first_block.hash:
                print("first block hash doesn't correspond")
                return False

        return True

    @staticmethod
    def is_valid_block(block: Block, previous_block: Block, check_hash=True):
        if previous_block.index + 1 != block.index:
            return False

        if block.previous_hash is None or block.previous_hash != previous_block.hash:
            return False

        if block.hash is None:
            return False

        if check_hash:
            if calculate_hash(block) != block.hash:
                return False

        return True

    def is_block_chain_valid(self, check_hash=True):
        if not self.is_first_block_valid(check_hash):
            return False

        if not BlockChain.blocks:
            return True

        for i in range(1, len(BlockChain.blocks)):
            previous_block = BlockChain.blocks[i - 1]
            block = BlockChain.blocks[i]
            if not self.is_valid_block(block, previous_block, check_hash):
                print(f"block {i} not valid")
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
