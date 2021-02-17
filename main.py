from flask.cli import FlaskGroup

from app import create_app
from app import BlockChain

cli = FlaskGroup(create_app=create_app)


@cli.command("test_block_chain")
def test_block_chain():
    block_chain = BlockChain("First Block")

    block1 = block_chain.new_block("Second Block")
    block_chain.add_block(block1)

    block2 = block_chain.new_block("Third Block")
    block_chain.add_block(block2)

    block3 = block_chain.new_block("Fourth Block")
    block_chain.add_block(block3)

    print(len(BlockChain.blocks))

    print("Blockchain validity:", block_chain.is_block_chain_valid())

    print(block_chain.json())


if __name__ == "__main__":
    cli()
