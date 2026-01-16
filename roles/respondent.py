from crypto.elgamal import encrypt
from crypto.pedersen import commit
from crypto.zk_range import prove


class Respondent:
    def __init__(self, params):
        self.p, self.q, self.g, self.h, self.pk = params


    def rate(self, value):
        C1, C2 = encrypt(value, self.pk, self.p, self.q, self.g)
        com, r = commit(value, self.p, self.q, self.g, self.h)
        proof = prove(self.p, self.q, self.g, self.pk, C1, C2, r, value)
        return {"C1": C1, "C2": C2, "commitment": com, "proof": proof}