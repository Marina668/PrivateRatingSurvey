import random

class Polynomial:
    def __init__(self, coeffs, q):
        self.coeffs = coeffs
        self.q = q

    def eval(self, x):   # poly(x)
        res, power = 0, 1
        for c in self.coeffs:
            res = (res + c * power) % self.q
            power = (power * x) % self.q
        return res


def feldman_commit(coeffs, g, p):
    return [pow(g, c, p) for c in coeffs]


def verify_share(share, idx, commitments, g, p, q):
    lhs = pow(g, share, p)
    rhs, power = 1, 1
    for C in commitments:
        rhs = (rhs * pow(C, power, p)) % p
        power = (power * idx) % q
    return lhs == rhs


class DKGSession:
    def __init__(self, m, t, p, q, g):
        self.m, self.t, self.p, self.q, self.g = m, t, p, q, g
        self.polys = []
        self.commitments = []
        self.shares = {}


    def setup(self):
        for _ in range(self.m):
            coeffs = [random.randrange(self.q) for _ in range(self.t)]
            poly = Polynomial(coeffs, self.q)
            self.polys.append(poly)
            self.commitments.append(feldman_commit(coeffs, self.g, self.p))
        for i, poly in enumerate(self.polys, 1):
            for j in range(1, self.m + 1):
                self.shares.setdefault(j, []).append(poly.eval(j))


    def aggregated_shares(self):
        return {j: sum(v) % self.q for j, v in self.shares.items()}


    def public_key(self):
        pk = 1
        for c in self.commitments:
            pk = (pk * c[0]) % self.p
        return pk