from app.util import calculate_hash


def test_calculate_hash(block):
    _hash = calculate_hash(block)
    assert isinstance(_hash, str)

