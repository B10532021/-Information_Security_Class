import sys
from CaesarDecrypt import CaesarDecrypt
from PlayfairDecrypt import PlayfairDecrypt
from RailFenceDecrypt import RailFenceDecrypt
from RowTranspositionDecrypt import RowDecrypt
from VernamProposedTheAutokeySystemDecrypt import VernamDecrypt

def main():
    plainText = ''
    cipher = sys.argv[1]
    key = sys.argv[2]
    cipherText = sys.argv[3]
    if cipher == 'caesar':
        print(CaesarDecrypt(key, cipherText))
    elif cipher == 'playfair':
        print(PlayfairDecrypt(key, cipherText))
    elif cipher == 'vernam':
        print(VernamDecrypt(key, cipherText))
    elif cipher == 'row':
        print(RowDecrypt(key, cipherText))
    elif cipher == 'rail_fence':
        print(RailFenceDecrypt(key, cipherText))

if __name__ == '__main__':
    main()