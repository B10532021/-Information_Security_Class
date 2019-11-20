import os


BLOCK_SIZE = 32

INIT_VEC = os.urandom(BLOCK_SIZE) # Initialization Vector

KEY = os.urandom(BLOCK_SIZE)