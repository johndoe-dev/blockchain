from flask import Blueprint
from flask_restful import Api

from app.blockchain_api.views.blockchain import BlockChainApi

block_chain_blueprint = Blueprint("blockchain", __name__)
api = Api(block_chain_blueprint)


# init block_chain with a first block
api.add_resource(BlockChainApi, "/init")
