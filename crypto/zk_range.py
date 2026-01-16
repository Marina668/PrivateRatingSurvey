import random
import hashlib

def H(*args):
    h = hashlib.sha256()
    for a in args:
        h.update(str(a).encode())
    return int.from_bytes(h.digest(), 'big')


# OR-proof that value ∈ {0..10}
def prove(p, q, g, pk, C1, C2, r, value):
    proofs = {}
    challenges = {}

    real_k = value
    w_real = random.randrange(q)

    # --- simulate all k ≠ v ---
    for k in range(11):
        if k == real_k:
            continue

        c = random.randrange(q)
        z = random.randrange(q)

        C2k = (C2 * pow(g, -k, p)) % p

        a1 = (pow(g, z, p) * pow(C1, -c, p)) % p
        a2 = (pow(pk, z, p) * pow(C2k, -c, p)) % p

        proofs[k] = (a1, a2, c, z)
        challenges[k] = c

    # --- real proof ---
    a1_real = pow(g, w_real, p)
    a2_real = pow(pk, w_real, p)

    # Fiat–Shamir
    c_all = H(C1, C2, *sum(proofs.values(), ()), a1_real, a2_real) % q
    c_real = (c_all - sum(challenges.values())) % q
    z_real = (w_real + c_real * r) % q
    proofs[real_k] = (a1_real, a2_real, c_real, z_real)

    sliced_proofs = dict(list(proofs.items())[:11])
    return sliced_proofs


def verify(p, q, g, pk, rating):
    C1 = rating["C1"]
    C2 = rating["C2"]
    proofs = rating["proof"]

    one_true = []

    for k, (a1, a2, c, z) in proofs.items():
        C2k = (C2 * pow(g, -k, p)) % p

        lhs1 = pow(g, z, p)
        rhs1 = (a1 * pow(C1, c, p)) % p

        lhs2 = pow(pk, z, p)
        rhs2 = (a2 * pow(C2k, c, p)) % p

        one_true.append(lhs1 != rhs1 or lhs2 != rhs2)

    return any(one_true)