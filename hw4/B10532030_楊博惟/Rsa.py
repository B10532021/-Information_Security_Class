from math import gcd
import random
from Crypto.PublicKey import _RSA

def extend_gcd(a, b):
    """
    compute extend_gcd: ax + by = gcd(a, b) to generate x, y, gcd(a, b)
    :param a: coefficient
    :param b: coefficient
    :return: x, y, gcd(a, b)
    """
    if b == 0:  # find gcd
        return 1, 0, a
    else:
        x, y, g = extend_gcd(b, a % b)
        return y, (x - (a // b) * y), g


def modulo_inverse(base, modulus):
    x, y, g = extend_gcd(base, modulus)
    if g != 1:  # not coprime
        raise Exception('Inverse does not exist')
    else:
        return x % modulus


def square_and_multiply(base, exponent, modulus) -> int:
    """
    compute a^b in square with square-and-multiply algorithm
    """
    if exponent < 0:
        raise ValueError("Can't compute negative exponent")

    binary = bin(exponent).lstrip("0b")
    ret = 1
    for i in binary:
        ret = ret * ret % modulus
        if i == '1':
            ret = ret * base % modulus
    return ret


def miller_rabin_test(p, times=20):
    if p == 2 or p & 1 == 0:
        return False

    def find_components(n):
        u = 0
        while (n & 1 == 0):
            n >>= 1
            u += 1
        return u, n

    k, m = find_components(p - 1)
    for i in range(times):
        a = random.randrange(2, p - 2)
        b = square_and_multiply(a, m, p)
        if b != 1 and b != p - 1:
            for i in range(k - 1):
                if b == p - 1:
                    break
                b = b * b % p
                if b == 1:
                    return False
            if b != p - 1:
                return False
        return True


def get_prime(bits=512):
    while (True):
        n = random.getrandbits(bits)
        if miller_rabin_test(n):
            return n


def generate_key(bits=1024, e=65537):
    '''
    generate RSA key
    '''
    if bits & 1 == 1:
        raise ValueError("Don't use an odd number of bits for the key")

    p = get_prime()
    q = get_prime()
    n = p * q
    phi_n = (p - 1) * (q - 1)

    assert gcd(e, phi_n) == 1

    d = modulo_inverse(e, phi_n)

    return p, q, n, e, d


def encrypt(n, e, plaintext: str):
    """
    use prime n and e to encrypt plaintext by RSA algorithm
    :return: ciphertext after RSA encrypt
    """
    hex_str = plaintext.encode('ascii').hex()
    num = int(hex_str, 16)
    if num > n:
        raise Exception("RSA can't encrypt too long plaintext")

    ciphertext = square_and_multiply(num, e, n)

    return hex(ciphertext)


def decrypt(n, d, ciphertext: str):
    num = int(ciphertext, 16)
    plaintext_hex = f"{square_and_multiply(num, d, n):x}"
    plaintext = bytes.fromhex(plaintext_hex).decode('ascii')

    return plaintext


def main():
    while True:
        print(
            "1: generate key\n"
            "2: encrypt a plaintext\n"
            "3: decrypt a ciphertext\n"
        )
        option = int(input("select your choice: "))
        if option == 1:
           bits = int(input("key length(1024 bits is recommended): "))
           p, q, n, e, d = generate_key(bits)
           print(f"p: {hex(p)}\n"
                 f"q: {hex(q)}\n"
                 f"n: {hex(n)}\n"
                 f"e: {hex(e)}\n"
                 f"d: {hex(d)}")
        elif option == 2:
            n = int(input("n(hex string expected): "), 16)
            e = int(input("e(hex string expected): "), 16)
            plaintext = input("plaintext(must be shorter than the size of n): ")
            ciphertext = encrypt(n, e, plaintext)
            print(f"ciphertext(hex string): {ciphertext}")
        elif option == 3:
            n = int(input("n(hex string expected): "), 16)
            d = int(input("d(hex string expected): "), 16)
            ciphertext = input("ciphertext: ")
            plaintext = decrypt(n, d, ciphertext)
            print(f"plaintext: {plaintext}")
        else:
            print("select!!!!!!!!!")
        print('-'*100)


if __name__ == '__main__':
    main()

   
