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


def aes_decrypt(ciphertext: bytes, mode) -> bytes:
    text = pad(ciphertext)
    blocks = [text[i:i + BLOCK_SIZE] for i in range(0, len(text), BLOCK_SIZE)]

    if mode == 'ECB':
        plaintext = bytes().join([aes.decrypt(block) for block in blocks])
    if mode == 'CBC':
        plaintext = xor(aes.decrypt(blocks[0]), INIT_VEC)
        prev_cipher_block = blocks[0]
        for i in range(1, len(blocks)):
            plaintext += xor(aes.decrypt(blocks[i]), blocks[i-1])

    return plaintext


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

    with open(f'Key_{mode}', 'rb') as file:
        key = file.read()

    # decrypt
    aes = AES.new(key, AES.MODE_ECB)
    plaintext = aes_decrypt(arr, mode)
    # write encrypted image
    img = Image.open(io.BytesIO(header + plaintext[:original_len]))
    img.save(f'decrypt_{name}.png')
