from typing import List
from app.models import (
    BlockChain,
    Block,
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


def compare_block_chain(block_chain: BlockChain,
                        first_block_chain_json: List[dict],
                        second_block_chain_json: List[dict]) -> List[dict]:
    try:
        init_block_chain_from_list(block_chain, first_block_chain_json)
        first_block_chain = block_chain.get_block_chain()

        init_block_chain_from_list(block_chain, second_block_chain_json)
        second_block_chain = block_chain.get_block_chain()

    except BlockChainInvalid:
        raise BlockChainInvalid

    except BlockChainInvalidList:
        raise BlockChainInvalidList

    if len(first_block_chain) >= len(second_block_chain):
        return __compare_block_chain(block_chain, first_block_chain, second_block_chain)
    else:
        return __compare_block_chain(block_chain, second_block_chain, first_block_chain)


def __compare_block_chain(block_chain: BlockChain,
                          first_block_chain: List[Block],
                          block_chain_to_compare_with: List[Block]):
    to_add = []

    for index, block in enumerate(first_block_chain):
        try:
            if block.serialize() != block_chain_to_compare_with[index].serialize() or \
                    block.serialize()["data"] != block_chain_to_compare_with[index].serialize()["data"]:
                to_add.append(block_chain_to_compare_with[index].serialize()["data"])
        except IndexError:
            break

    init_block_chain_from_list(block_chain, [block.serialize() for block in first_block_chain])

    print("to_add", to_add)

    for data in to_add:
        add_block(block_chain, data)

    return block_chain.serialize()
