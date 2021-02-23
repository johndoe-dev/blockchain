from hashlib import sha512


def calculate_hash(block):
    bloc = str(block.index) + str(block.previous_hash) + str(block.timestamp) + str(block.data)
    return sha512(bloc.encode('utf-8')).hexdigest()
