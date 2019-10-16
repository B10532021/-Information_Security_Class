import argparse

from const import *

parser = argparse.ArgumentParser()
parser.add_argument('key')
parser.add_argument('plaintext')


class DESDecrypt:
    def __init__(self, key, block):
        self.block = block
        self.key = key

    def decrypt(self):
        block = self.permute(self.block, 64, IP)
        # l為block往右平移32個bit, r = block & 0x00000000ffffffff
        l, r = block >> 32, block & 0xffffffff
        for key in self.derive_keys():
            l, r = r, l ^ self.f(r, key)

        return self.permute(r << 32 | l, 64, IP_1)

    # 將cipher內容交換位置
    def permute(self, block, size, table):
        ret = 0
        # i = 0~63, j = table內容1~64
        for i, j in enumerate(table):
            if block & (1 << size - j):
                ret |= 1 << (len(table) - 1 - i)

        return ret

    # 取得每個階段的key
    def derive_keys(self):
        # k 為56個bits
        k = self.permute(self.key, 64, PC_1)

        C, D = k >> 28, k & 0xfffffff
        yield self.permute(C << 28 | D, 56, PC_2)
        for x in ROTATES[1:]:  
            C, D = self.rotate_right(C, x), self.rotate_right(D, x)
            # yield可以使每做一次迴圈就先回傳一個new key等又call到這個func時繼續接著做for
            yield self.permute(C << 28 | D, 56, PC_2)
            

    def f(self, block, key):
        # 與E做擴展置換48, 與key做xor
        block = self.permute(block, 32, E) ^ key
        substitution = self.substitute(block)
        permutation = self.permute(substitution, 32, P)
        return permutation

    def substitute(self, block):
        ret = 0
        for i, box in enumerate(S_BOX):
            # 42是因為第一次需要右移42個bit，而i是從0開始。因此不是48
            sub_6 = block >> (42 - i * 6) & 0b111111
            # 將row以5、6bit代表可以知道是0~3的哪一row
            row = sub_6 & 0b100000 | (sub_6 & 1) << 4
            # col以前4個bit代表row中的哪一個位置
            col = (sub_6 & 0b011110) >> 1
            ret = (ret << 4) | box[row | col]

        return ret
    
    def rotate_right(self, k, i):
        # 循環右移 key 往右平移x個bits就在左邊補上x個原來右邊的x個bit
        if i == 1:
            return (k >> i) & 0xfffffff | (k & 1) << (28 - i)
        elif i == 2:
            return (k >> i) & 0xfffffff | (k & 3) << (28 - i)


if __name__ == '__main__':
    args = parser.parse_args()
    key = int(args.key[2:], 16)
    ciphertext = int(args.plaintext[2:], 16)

    des = DESDecrypt(key, ciphertext)
    print(f'0x{des.decrypt():X}'.lower())