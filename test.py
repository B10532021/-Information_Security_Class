import unittest

from Encrypt import caesar_cipher, playfair_cipher, vernam_cipher, row_cipher, rail_fence_cipher
from CaesarDecrypt import CaesarDecrypt
from PlayfairDecrypt import PlayfairDecrypt
from RailFenceDecrypt import RailFenceDecrypt
from RowTranspositionDecrypt import RowDecrypt
from VernamProposedTheAutokeySystemDecrypt import VernamDecrypt


class TestEncryptDecrypt(unittest.TestCase):
    def test_caesar(self):
        key = '5'
        plaintext = 'doyourbestandthenletgo'
        cipher = caesar_cipher(int(key), plaintext)
        self.assertEqual(CaesarDecrypt(int(key), cipher), plaintext)

    def test_playfair(self):
        key = 'COMP'
        plaintext = 'doyourbestandthenletgo'
        cipher = playfair_cipher(key, plaintext)
        self.assertEqual(PlayfairDecrypt(key, cipher), plaintext)

    def test_vernam(self):
        key = 'TEC'
        plaintext = 'doyourbestandthenletgo'
        cipher = vernam_cipher(key, plaintext)
        self.assertEqual(VernamDecrypt(key, cipher), plaintext)

    def test_row(self):
        key = '45362178'
        plaintext = 'doyourbestandthenletgo'
        cipher = row_cipher(key, plaintext)
        self.assertEqual(RowDecrypt(key, cipher), plaintext)

    def test_rail_fence(self):
        key = '2'
        plaintext = 'doyourbestandthenletgo'
        cipher = rail_fence_cipher(int(key), plaintext)
        self.assertEqual(RailFenceDecrypt(int(key), cipher), plaintext)


if __name__ == '__main__':
    unittest.main()
