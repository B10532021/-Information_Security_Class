from argparse import ArgumentParser
import io
import os

from PIL import Image
from Crypto.Cipher import AES

from config import *
from utils import *


parser = ArgumentParser()
parser.add_argument('img_path')
parser.add_argument('mode', choices=['ECB', 'CBC'])
#parser.add_argument('--key', '-k', help='key for AES encryption')


def aes_encrypt(plaintext: bytes, mode) -> bytes:
    text = pad(plaintext)
    blocks = [text[i:i + BLOCK_SIZE] for i in range(0, len(text), BLOCK_SIZE)]

    if mode == 'ECB':
        cipher = bytes().join([aes.encrypt(block) for block in blocks])
    if mode == 'CBC':
        cipher = aes.encrypt(xor(blocks[0], INIT_VEC))
        prev_cipher_block = cipher
        for i in range(1, len(blocks)):
            prev_cipher_block = aes.encrypt(xor(prev_cipher_block, blocks[i]))
            cipher += prev_cipher_block

    return cipher


if __name__ == '__main__':
    args = parser.parse_args()
    img_path = args.img_path
    mode = args.mode

    # convert .jpg/.png to .ppm 
    im = Image.open(img_path).convert('RGB')
    name = img_path.rsplit('.', 1)[0]
    im.save(f"{name}.ppm")

    # get image bytes array
    with open(f"{name}.ppm", 'rb') as file:
        header = file.readline() + file.readline() + file.readline()
        arr = file.read()
        original_len = len(arr)

    # encrypt
    aes = AES.new(KEY, AES.MODE_ECB)
    cipher = aes_encrypt(arr, mode)

    # write encrypted image
    img = Image.open(io.BytesIO(header + cipher[:original_len]))
    img.save(f'{name}_{mode}.png')
