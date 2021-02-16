import pytest
from tests.fixtures import fixture_bloc


@pytest.fixture()
def block():
    return fixture_bloc.fixture_block()


@pytest.fixture()
def expected_result_block_chain():
    return fixture_bloc.fixture_expected_result_block_chain
