import random
from typing import Tuple

def is_prime(n: int, k: int = 12) -> bool:
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if is_prime(p):
            return p


def generate_group(bits: int = 128) -> Tuple[int, int, int, int]:
    while True:
        q = generate_prime(bits - 1)
        p = 2 * q + 1
        if is_prime(p):
            break

    def find_elem():
        for _ in range(2000):
            a = random.randrange(2, p - 1)
            x = pow(a, 2, p)
            if x != 1 and pow(x, q, p) == 1:
                return x
        raise RuntimeError("failed find generator")

    g = find_elem()
    h = find_elem()
    while h == g:
        h = find_elem()
    return p, q, g, h