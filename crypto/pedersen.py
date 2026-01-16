import random

def commit(value, p, q, g, h):
    r = random.randrange(1, q)
    com = (pow(g, value, p) * pow(h, r, p)) % p
    return com, r