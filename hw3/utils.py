from PIL import Image

from config import *


def xor(b1: bytes, b2: bytes) -> bytes:
    ''' XOR two bytes objects '''
    ret = bytearray(b1)
    for i, b in enumerate(b2):
        ret[i] ^= b
    return bytes(ret)


def pad(text: bytes):
	padding = BLOCK_SIZE - (len(text) % BLOCK_SIZE)
	return text + bytes([padding] * padding)


def unpad(text: bytes):
	padding = text[-1]
	return text[:-padding]
