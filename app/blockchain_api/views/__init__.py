from flask import Blueprint
from flask_restful import Api

from app.blockchain_api.views.blockchain import BlockChainInitApi, BlockChainApi, BlockChainCompareApi

block_chain_blueprint = Blueprint("blockchain", __name__)
api = Api(block_chain_blueprint)


# init block_chain with a first block
api.add_resource(BlockChainInitApi, "/init")

# add block to blockchain
api.add_resource(BlockChainApi, "/add")

# compare and concatenate 2 blockchains
api.add_resource(BlockChainCompareApi, "/compare")
