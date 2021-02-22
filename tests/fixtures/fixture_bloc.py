from app.models import Block
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


def fixture_expected_serialized_block(new_block):
    return {
        "index": new_block.index,
        "previous_hash": new_block.previous_hash,
        "timestamp": str(new_block.timestamp),
        "data": new_block.data,
        "hash": new_block.hash
    }


def fixture_expected_serialized_block_chain(block_chain):
    return [fixture_expected_serialized_block(block) for block in block_chain]


def fixture_expected_block_chain_json():
    return [
        {
            "index": 0,
            "previous_hash": None,
            "timestamp": "2021-02-18 13:29:20.045029",
            "data": "first block",
            "hash": "c7a373b2c7ee2d815917fc3d7fe72e1be31441b1474f5fa338a3c48f04afa7d1"
        },
        {
            "index": 1,
            "previous_hash": "c7a373b2c7ee2d815917fc3d7fe72e1be31441b1474f5fa338a3c48f04afa7d1",
            "timestamp": "2021-02-18 13:29:20.045066",
            "data": "second block",
            "hash": "c31c419bcb207b519465703273124291b0df4de9b4484e14b8fa0f047399bc2d"
        },
        {
            "index": 2,
            "previous_hash": "c31c419bcb207b519465703273124291b0df4de9b4484e14b8fa0f047399bc2d",
            "timestamp": "2021-02-18 13:29:20.045075",
            "data": "third block",
            "hash": "6336ddb3e9bbb40ad60561ab3557d40132d234a98a048bfd3d707b68f68edd17"
        },
        {
            "index": 3,
            "previous_hash": "6336ddb3e9bbb40ad60561ab3557d40132d234a98a048bfd3d707b68f68edd17",
            "timestamp": "2021-02-18 13:29:20.045081",
            "data": "fourth block",
            "hash": "b663e1ed33b4e38fd336d3114345eb07936d732d608cb3a347d450f8a5480ad3"
        }
    ]


def fixture_block_data():
    return ["first block", "second block", "third block", "fourth block"]
