from flask import request, current_app
from flask_restful import Resource
from http import HTTPStatus
from app.models import (
    BlockChain,
    BlockChainNotInitializedError,
    BlockChainDataInvalid,
    BlockChainInvalid,
    BlockChainInvalidList)
from app.blockchain_api.controllers import blockchain_controller
from app.blockchain_api.exceptions import DataMissingKeyError, DataTypeError

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
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalid as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalidList as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST

        return result, HTTPStatus.CREATED


class BlockChainApi(Resource):
    def post(self):

        data = request.get_json()

        try:
            result = blockchain_controller.add_block(block_chain, data)
        except BlockChainNotInitializedError as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainDataInvalid as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST

        return result, HTTPStatus.CREATED


class BlockChainCompareApi(Resource):
    def post(self):

        data = request.get_json()

        try:
            try:
                first_block_chain = data["first_block_chain"]
                second_block_chain = data["second_block_chain"]
            except KeyError as e:
                raise DataMissingKeyError(f"Data miss keys : {str(e)}")
            except TypeError as e:
                raise DataTypeError(f"Data must be a 'dict' with keys"
                                    f" 'first_block_chain' and 'second_block_chain' but  was {type(data)}")

            result = blockchain_controller.compare_block_chain(block_chain, first_block_chain, second_block_chain)

        except DataMissingKeyError as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except DataTypeError as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalid as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST
        except BlockChainInvalidList as e:
            current_app.logger.error(e.message)
            return e.message, HTTPStatus.BAD_REQUEST

        return result, HTTPStatus.CREATED
