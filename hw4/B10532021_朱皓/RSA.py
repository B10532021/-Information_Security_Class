from argparse import ArgumentParser
from math import gcd
import random

parser = ArgumentParser()
parser.add_argument('mode', choices=['init', 'encrypt', 'decrypt'], help='Choose the operate mode')

def MillerRabinTest(num):
    if num == 2 or num == 3:
        return True
    if num % 2 == 0:
        return False

    m = num - 1
    k = 0
    while m % 2 == 0:
        m = m // 2
        k += 1

    for trials in range(5):
        a = random.randrange(2, num - 2)
        b = SquareAndMultiply(a, m, num)
        if b != 1 and b != (num - 1):
            i = 1
            while i < k and b != num - 1:
                b = (b ** 2) % num
                if b == 1:
                    return False
                i += 1
            if b != num -1:
                return False
    return True


def SquareAndMultiply(base, exponent, modulus):
    if exponent < 0:
        return
    
    binary = f'{exponent:b}'
    y = 1
    for i in binary:
        y = (y ** 2) % modulus
        if i == '1':
            y = y * base % modulus
    return y

def ExtendedEuclidean(a, b):
    if a == 0: 
        return (b, 0, 1) 
    else: 
        g, y, x = ExtendedEuclidean(b % a, a) 
        return (g, x - (b // a) * y, y) 

def FindModInverse(num, modulus):
    g, x, y = ExtendedEuclidean(num, modulus) 
    return x % modulus

def GetPrime(bits = 1024):
    prime = random.getrandbits(bits)
    while not MillerRabinTest(prime):
        prime = random.getrandbits(bits)

    return prime

def ChineseRemainderTheorem(ciphertext, d, p, q):
    Xp = ciphertext % p
    Xq = ciphertext % q
    Dp = d % (p - 1)
    Dq = d % (q - 1)
    Mp = SquareAndMultiply(Xp, Dp, p)
    Mq = SquareAndMultiply(Xq, Dq, q)
    Pinv = FindModInverse(p, q)
    T = Pinv % q
    U = ((Mq- Mp) * T) % q
    plaintext = Mp + p * U
    
    return plaintext

def GenerateKey(bits = 1024):
    p = GetPrime(bits // 2)
    q = GetPrime(bits // 2)
    n = p * q
    fn = (p - 1) * (q - 1)
    while True:
        e = random.randrange(1, fn)
        if gcd(e, fn) == 1:
            break
    d = FindModInverse(e, fn)
    return p, q, n, e, d

def Encrypt(plaintext, n, e):
    ciphertext = SquareAndMultiply(plaintext, e, n)
    return hex(ciphertext)

def Decrypt(ciphertext, d, p, q):
    plaintext = ChineseRemainderTheorem(ciphertext, d, p, q)
    plaintext = bytes.fromhex(f'{plaintext:x}').decode('ascii')
    return plaintext


def main():
    args = parser.parse_args()
    mode = args.mode

    if mode == 'init':
        bits_length = int(input('please enter bits length：'))
        p, q, n, e, d = GenerateKey(bits_length)
        print(f"p: {hex(p)}")
        print(f"q: {hex(q)}")
        print(f"n: {hex(n)}")
        print(f"e: {hex(e)}")
        print(f"d: {hex(d)}")
        return
    elif mode == 'encrypt':
        plaintext = int(input('please enter plaintext：').encode('ascii').hex(), 16)
        n = int(input('please enter n：'), 16)
        e = int(input('please enter e：'), 16)
        ciphertext = Encrypt(plaintext, n, e)
        print('ciphertext：{0}'.format(ciphertext))
        return
    elif mode == 'decrypt':
        ciphertext = int(input('please enter ciphertext：'), 16)
        # n = int(input('please enter n：'), 16)
        d = int(input('please enter d：'), 16)
        p = int(input('please enter p：'), 16)
        q = int(input('please enter q：'), 16)
        plaintext = Decrypt(ciphertext, d, p, q)
        print('plaintext：{0}'.format(plaintext))
        return

if __name__ == "__main__":
    main()