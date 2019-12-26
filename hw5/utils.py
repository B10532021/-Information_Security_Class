import random


def extend_gcd(a: int, b: int):
    """
    compute extend_gcd: ax + by = gcd(a, b) to generate x, y, gcd(a, b)
    :param a: integer1
    :param b: integer2
    :return: x, y, gcd(a, b)
    """
    if b == 0:  # find gcd
        return 1, 0, a
    else:
        # compute sub Extend Euclidean algorithm
        x, y, g = extend_gcd(b, a % b)
        return y, (x - (a // b) * y), g


def modulo_inverse(base: int, divisor: int) -> int:
    """
    find the x that (base * x) and 1 congruent modulo divisor
    x = base ^ -1 mod divisor
    :param base: int
    :param divisor:int, the divisor
    :return: int
    """
    x, y, g = extend_gcd(base, divisor)
    if g != 1:  # not coprime
        raise Exception('Inverse does not exist')
    else:
        return x % divisor


def square_and_multiply(base: int, exponent: int, divisor: int) -> int:
    """
    compute a^b in square with square-and-multiply algorithm
    proof:
        7 ^ 11
        bin(11) = 1011
        7 ^ 11 = (((((1 ^ 2 * 7) ^ 2) ^ 2) * 7) ^ 2) * 7
    :param base: int
    :param exponent: int
    :param divisor: int
    :return: int, base ^ exponent % divisor
    """
    if exponent < 0:
        raise ValueError("Can't compute negative exponent")

    binary = bin(exponent).lstrip("0b")  # convert the exponent into binary
    result = 1
    for i in binary:
        result = result * result % divisor
        if i == '1':
            result = result * base % divisor

    return result


def miller_rabin_test(p: int, times=30) -> bool:
    """
    to test p is prime or not
    :param p: int
    :param times: int
    :return: bool
    """
    if p == 2:
        return True

    if p & 1 == 0:
        return False

    def find_components(n):
        """
        convert n = 2 ^ u * v
        :param n: int
        :return: (int, int)
        """
        u = 0
        while (n & 1 == 0):
            n >>= 1
            u += 1
        return u, n

    k, m = find_components(p - 1)
    for i in range(times):
        a = random.randrange(2, p - 2)
        b = pow(a, m, p)
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


def generate_prime(bits: int):
    """
    generate large prime
    """
    while (True):
        n = random.randrange(2**(bits-1), 2**bits)
        if miller_rabin_test(n):
            return n
