from crypto.zk_range import verify


class Verifier:
    def __init__(self, p, q, g, h, pk):
        self.p, self.q, self.g, self.h, self.pk = p, q, g, h, pk


    def verify_rating(self, rating_data):
        return verify(self.p, self.q, self.g, self.pk, rating_data)