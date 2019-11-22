from argparse import ArgumentParser
import io
import os

from PIL import Image
from Crypto.Cipher import AES

from config import *
from utils import *


parser = ArgumentParser()
parser.add_argument('img_path')
parser.add_argument('mode', choices=['ECB', 'CBC', 'CTR'])
#parser.add_argument('--key', '-k', help='key for AES encryption')


def aes_decrypt(ciphertext: bytes, mode) -> bytes:
    text = pad(ciphertext)
    blocks = [text[i:i + BLOCK_SIZE] for i in range(0, len(text), BLOCK_SIZE)]

    if mode == 'ECB':
        plaintext = bytes().join([aes.decrypt(block) for block in blocks])

    elif mode == 'CBC':
        with open(f'INIT_VEC_{mode}', 'rb') as file:
            init_vec = file.read()
        plaintext = xor(aes.decrypt(blocks[0]), init_vec)
        prev_cipher_block = blocks[0]
        for i in range(1, len(blocks)):
            plaintext += xor(aes.decrypt(blocks[i]), blocks[i-1])

    elif mode == 'CTR':
        with open(f'INIT_VEC_{mode}', 'rb') as file:
            init_vec = file.read()
        
        plaintext = xor(blocks[0], aes.encrypt(init_vec))
        for i in range(1, len(blocks)):
            counter = (int(init_vec.hex(), 16) + i) % ((1 << 256) - 1)
            plaintext += xor(blocks[i], aes.encrypt(counter.to_bytes(32, byteorder="big")))

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
    os.remove(f"{name}.ppm")

    with open(f'Key_{mode}', 'rb') as file:
        key = file.read()

    # decrypt
    aes = AES.new(key, AES.MODE_ECB)
    plaintext = aes_decrypt(arr, mode)
    # write decrypted image
    img = Image.open(io.BytesIO(header + plaintext[:original_len]))
    img.save(f'{name}_Decrypt.png')
