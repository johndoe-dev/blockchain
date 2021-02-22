import os
import pytest
from app import create_app
from tests.fixtures import fixture_bloc, fixture_data
from app.models import BlockChain


@pytest.fixture()
def data():
    return fixture_data.fixture_data()


@pytest.fixture()
def block():
    return fixture_bloc.fixture_block()


@pytest.fixture()
def expected_serialized_block():
    return fixture_bloc.fixture_expected_serialized_block


@pytest.fixture()
def expected_serialized_block_chain():
    return fixture_bloc.fixture_expected_serialized_block_chain


@pytest.fixture()
def expected_result_block_chain():
    return fixture_bloc.fixture_expected_result_block_chain


@pytest.fixture()
def expected_block_chain_json():
    return fixture_bloc.fixture_expected_block_chain_json()


@pytest.fixture()
def block_data():
    return fixture_bloc.fixture_block_data()


@pytest.fixture()
def block_chain_json():
    path_file = os.path.join(os.path.dirname(__file__), "fixtures", "test_blockchain.json")
    return path_file


@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        yield app
        BlockChain.blocks = []
