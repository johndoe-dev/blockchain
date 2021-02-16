from app import Block
from datetime import datetime


def fixture_block():
    return Block(0, None, datetime.now(), "fake block")


def fixture_expected_result_block_chain(new_block_chain):
    return "Block #0 [" + \
          "\n\tindex: 0" + \
          "\n\tprevious hash: None" + \
          f"\n\ttimestamp: {new_block_chain.blocks[0].timestamp}" + \
          "\n\tdata: first block" + \
          f"\n\thash: {new_block_chain.blocks[0].hash}" + \
          "\n]\n\n" + \
          "Block #1 [" + \
          "\n\tindex: 1" + \
          f"\n\tprevious hash: {new_block_chain.blocks[1].previous_hash}" + \
          f"\n\ttimestamp: {new_block_chain.blocks[1].timestamp}" + \
          "\n\tdata: second block" + \
          f"\n\thash: {new_block_chain.blocks[1].hash}" + \
          "\n]\n\n" + \
          "Block #2 [" + \
          "\n\tindex: 2" + \
          f"\n\tprevious hash: {new_block_chain.blocks[2].previous_hash}" + \
          f"\n\ttimestamp: {new_block_chain.blocks[2].timestamp}" + \
          "\n\tdata: third block" + \
          f"\n\thash: {new_block_chain.blocks[2].hash}" + \
          "\n]\n\n" + \
          "Block #3 [" + \
          "\n\tindex: 3" + \
          f"\n\tprevious hash: {new_block_chain.blocks[3].previous_hash}" + \
          f"\n\ttimestamp: {new_block_chain.blocks[3].timestamp}" + \
          "\n\tdata: fourth block" + \
          f"\n\thash: {new_block_chain.blocks[3].hash}" + \
          "\n]\n\n"
