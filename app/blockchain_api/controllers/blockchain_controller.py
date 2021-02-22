from typing import List
from app.models import (
    BlockChain,
    BlockChainAlreadyInitError,
    BlockChainDataInvalid,
    BlockChainNotInitializedError,
    BlockChainInvalid,
    BlockChainInvalidList)


def init_block_chain(block_chain: BlockChain, payload: dict) -> List[dict]:
    try:
        block_chain.init_first(payload)
    except BlockChainAlreadyInitError:
        add_block(block_chain, payload)
    except BlockChainDataInvalid:
        raise BlockChainDataInvalid

    return block_chain.serialize()


def add_block(block_chain: BlockChain, payload: dict) -> List[dict]:
    try:
        new_block = block_chain.new_block(payload)
        block_chain.add_block(new_block)
    except BlockChainNotInitializedError:
        raise BlockChainNotInitializedError
    except BlockChainDataInvalid:
        raise BlockChainDataInvalid

    return block_chain.serialize()


def init_block_chain_from_list(block_chain: BlockChain, payload: List[dict]) -> List[dict]:
    try:
        block_chain.init_from_list_of_dict(payload)
    except BlockChainInvalid:
        raise BlockChainInvalid
    except BlockChainInvalidList:
        raise BlockChainInvalidList

    return block_chain.serialize()
