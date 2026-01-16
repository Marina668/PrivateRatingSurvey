from crypto.dkg import DKGSession
from crypto.elgamal import aggregate

def lagrange_coeff(j, S, q):
    """
    Lagrange coefficient λ_j for index j
    S = list of indices
    """
    num, den = 1, 1
    for k in S:
        if k == j:
            continue
        num = (num * (-k)) % q
        den = (den * (j - k)) % q
    return num * pow(den, -1, q) % q


class Organizer:
    def __init__(self, p, q, g):
        self.p, self.q, self.g = p, q, g


    def collect(self, ratings):
        cts = [(r["C1"], r["C2"]) for r in ratings]
        return aggregate(cts, self.p), len(cts)


    def combine_decryptions(self, partials, indices, C2_agg):
        D = 1
        for Di, j in zip(partials, indices):
            l = lagrange_coeff(j, indices, self.q)
            D = (D * pow(Di, l, self.p)) % self.p

        return (C2_agg * pow(D, -1, self.p)) % self.p


    def decode_result(self, n, M):
        max_sum = n * 10
        recovered_sum = None

        for x in range(max_sum + 1):
            if pow(self.g, x, self.p) == M:
                return x
        return recovered_sum