from flask import request
from flask_restful import Resource
from http import HTTPStatus
from app import BlockChain


class BlockChainApi(Resource):
    def post(self):

        data = request.get_json()

        blockchain = BlockChain(data)

        return blockchain.serialize(), HTTPStatus.CREATED
