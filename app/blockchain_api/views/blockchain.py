from flask import request
from flask_restful import Resource
from http import HTTPStatus
from app.models import (
    BlockChain,
    BlockChainNotInitializedError,
    BlockChainDataInvalid,
    BlockChainInvalid,
    BlockChainInvalidList)
from app.blockchain_api.controllers import blockchain_controller

block_chain = BlockChain()


class BlockChainInitApi(Resource):
    def post(self):

        data = request.get_json()
        from_json = "from_json" in request.args

        try:
            if from_json:
                result = blockchain_controller.init_block_chain_from_list(block_chain, data)
            else:
                result = blockchain_controller.init_block_chain(block_chain, data)
        except BlockChainDataInvalid as e:
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalid as e:
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalidList as e:
            return e.message, HTTPStatus.BAD_REQUEST

        return result, HTTPStatus.CREATED


class BlockChainApi(Resource):
    def post(self):

        data = request.get_json()

        try:
            result = blockchain_controller.add_block(block_chain, data)
        except BlockChainNotInitializedError as e:
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainDataInvalid as e:
            return e.message, HTTPStatus.BAD_REQUEST

        return result, HTTPStatus.CREATED
