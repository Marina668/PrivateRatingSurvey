import random

def encrypt(value, pk, p, q, g):
    k = random.randrange(1, q)
    C1 = pow(g, k, p)
    C2 = (pow(pk, k, p) * pow(g, value, p)) % p
    return C1, C2


def aggregate(ciphertexts, p):
    C1 = 1
    C2 = 1
    for c1, c2 in ciphertexts:
        C1 = (C1 * c1) % p
        C2 = (C2 * c2) % p
    return C1, C2