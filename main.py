from app import BlockChain

if __name__ == "__main__":
    block_chain = BlockChain()

    block1 = block_chain.new_block("Second Block")
    block_chain.add_block(block1)

    block2 = block_chain.new_block("Third Block")
    block_chain.add_block(block2)

    block3 = block_chain.new_block("Fourth Block")
    block_chain.add_block(block3)

    print("Blockchain validity:", block_chain.is_block_chain_valid())

    print(str(block_chain))
