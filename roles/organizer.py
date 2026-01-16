from crypto.dkg import DKGSession
from crypto.elgamal import aggregate


class Organizer:
    def __init__(self, p):
        self.p = p


    def collect(self, ratings):
        cts = [(r["C1"], r["C2"]) for r in ratings]
        return aggregate(cts, self.p), len(cts)