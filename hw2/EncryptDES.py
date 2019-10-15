import argparse

from const import *

parser = argparse.ArgumentParser()
parser.add_argument('key')
parser.add_argument('plaintext')


class DES:
    def __init__(self, key, block):
        self.block = block
        self.key = key

    def encrypt(self):
        block = self.permute(self.block, 64, IP)
        l, r = block >> 32, block & 0xffffffff
        for key in self.derive_keys():
            l, r = r, l ^ self.f(r, key)

        return self.permute(r << 32 | l, 64, IP_1)

    def permute(self, block, size, table):
        ret = 0
        for i, j in enumerate(table):
            if block & (1 << size - j):
                ret |= 1 << (len(table) - 1 - i)

        return ret

    def derive_keys(self):
        k = self.permute(self.key, 64, PC_1)

        C, D = k >> 28, k & 0xfffffff
        for x in ROTATES:
            C, D = self.rotate_left(C, x), self.rotate_left(D, x)
            yield self.permute(C << 28 | D, 56, PC_2)

    def f(self, block, key):
        block = self.permute(block, 32, E) ^ key
        substitution = self.substitute(block)
        permutation = self.permute(substitution, 32, P)
        return permutation

    def substitute(self, block):
        ret = 0
        for i, box in enumerate(S_BOX):
            sub_6 = block >> (42 - i * 6) & 0b111111
            row = sub_6 & 0b100000 | (sub_6 & 1) << 4
            col = (sub_6 & 0b011110) >> 1
            ret = (ret << 4) | box[row | col]

        return ret

    def rotate_left(self, k, i):
        return (k << i) & 0xfffffff | k >> (28 - i)


if __name__ == '__main__':
    args = parser.parse_args()
    key = int(args.key[2:], 16)
    plaintext = int(args.plaintext[2:], 16)

    des = DES(key, plaintext)
    print(f'0x{des.encrypt():X}')
