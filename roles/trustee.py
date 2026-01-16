class Trustee:
    def __init__(self, idx, share, p):
        self.idx = idx
        self.share = share
        self.p = p


    def partial_decrypt(self, C1):
        return self.idx, pow(C1, self.share, self.p)