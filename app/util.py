from hashlib import sha256


def calculate_hash(block):
    bloc = str(block.index) + str(block.previous_hash) + str(block.timestamp) + str(block.data)
    return sha256(bloc.encode('utf-8')).hexdigest()
