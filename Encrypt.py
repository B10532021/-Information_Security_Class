import argparse
from collections import OrderedDict
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('cipher', choices=[
                    'caesar', 'playfair', 'vernam', 'row', 'rail_fence'])
parser.add_argument('key')
parser.add_argument('plaintext')


def caesar_cipher(key: int, plaintext: str):
    cipher = ''
    for char in plaintext:
        if char == ' ':
            cipher += char
        elif char.isupper():
            cipher += chr((ord(char) + key - 65) % 26 + 65)
        else:
            cipher += chr((ord(char) + key - 97) % 26 + 97)

    return cipher.upper()


def playfair_cipher(key: str, plaintext: str):
    alphabet = 'abcdefghiklmnopqrstuvwxyz'

    key = key.replace('j', 'i')
    key = ''.join(OrderedDict.fromkeys(key + alphabet)).lower()
    key_matrix = np.reshape([c for c in key], (5, 5))

    position = {}
    for i in range(5):
        for j in range(5):
            position[key[i*5+j]] = (i, j)

    cipher = ''
    text_pair = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]
    for p in text_pair:
        r1, c1 = position[p[0]]
        r2, c2 = position[p[1]]
        if p[0] == p[1]:
            r2, c2 = position['x']

        if r1 == r2:
            cipher += key_matrix[r1][(c1+1) % 5]
            cipher += key_matrix[r2][(c2+1) % 5]
        elif c1 == c2:
            cipher += key_matrix[(r1+1) % 5][c1]
            cipher += key_matrix[(r2+1) % 5][c2]
        else:
            cipher += key_matrix[r1][c2]
            cipher += key_matrix[r2][c1]

    return cipher


def vernam_cipher(key: str, plaintext: str):
    cipher = ''
    i = 0
    key = key.lower()
    for char in plaintext.lower():
        cipher += chr(((ord(char)-97) ^ (ord(key[i])-97)) + 97)
        i += 1
        if i == len(key):
            i = 0

    return cipher.upper()


def row_cipher(key: str, plaintext: str):
    n = len(key)
    rows = [plaintext[i:i+n] for i in range(0, len(plaintext), n)]
    order = np.argsort([i for i in key])

    cipher = ''
    for idx in order:
        for row in rows:
            if idx < len(row):
                cipher += row[idx]

    return cipher.upper()


def rail_fence_cipher(key: int, plaintext: str):
    cipher = ''
    for i in range(key):
        for j in range(i, len(plaintext), key):
            cipher += plaintext[j]

    return cipher.upper()


if __name__ == '__main__':
    args = parser.parse_args()
    cipher = args.cipher
    key = args.key
    plaintext = args.plaintext

    if cipher == 'caesar':
        print(caesar_cipher(int(key), plaintext))
    elif cipher == 'playfair':
        print(playfair_cipher(key, plaintext))
    elif cipher == 'vernam':
        print(vernam_cipher(key, plaintext))
    elif cipher == 'row':
        print(row_cipher(key, plaintext))
    elif cipher == 'rail_fence':
        print(rail_fence_cipher(int(key), plaintext))
