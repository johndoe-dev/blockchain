import pytest
from app import create_app
from tests.fixtures import fixture_bloc, fixture_data
from app import BlockChain


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


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app
        BlockChain.blocks = []
