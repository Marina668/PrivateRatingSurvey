from crypto.group import generate_group
from crypto.dkg import DKGSession
from roles.respondent import Respondent
from roles.organizer import Organizer
from roles.trustee import Trustee
from roles.verifier import Verifier


def main():
    print("=== 1. Generate group parameters ===")
    p, q, g, h = generate_group(128)
    print("Group generated")
    print()

    print("=== 2. Distributed Key Generation (DKG) ===")
    m = int(input("Input number of respondents: "))   # number of trustees
    t = 2   # threshold

    dkg = DKGSession(m, t, p, q, g)
    dkg.setup()

    pk = dkg.public_key()
    shares = dkg.aggregated_shares()

    print("Public key pk =", pk)
    print("Trustee shares:", shares)
    print()

    trustees = [
        Trustee(idx, share, p)
        for idx, share in shares.items()
    ]

    print("=== 3. Respondents submit ratings ===")
    respondents = [Respondent((p, q, g, h, pk)) for _ in range(m)]

    ratings_input = input(f"Input {m} ratings: ")
    ratings_values = list(map(int, ratings_input.split()))
    ratings = []

    for rating_value, respondent in zip(ratings_values, respondents):
        rating = respondent.rate(rating_value)
        ratings.append(rating)
        print(f"Rating submitted: {rating_value}")

    print()

    print("=== 4. Verify zero-knowledge range proofs ===")
    verifier = Verifier(p, q, g, h, pk)
    verified_ratings = []

    for i, r_data in enumerate(ratings):
        is_valid = verifier.verify_rating(r_data)
        print(f"Rating {i + 1} valid: {is_valid}")
        if is_valid:
            verified_ratings.append(r_data)


    print()

    print("=== 5. Aggregate encrypted ratings ===")
    organizer = Organizer(p, q, g)
    (C1_agg, C2_agg), n = organizer.collect(verified_ratings)

    print("Aggregated ciphertext:")
    print("C1 =", C1_agg)
    print("C2 =", C2_agg)
    print("Number of ratings =", n)
    print()

    print("=== 6. Threshold decryption ===")
    selected_trustees = trustees[:t]

    partials = []
    indices = []

    for tr in selected_trustees:
        idx, Di = tr.partial_decrypt(C1_agg)
        partials.append(Di)
        indices.append(idx)
        print(f"Trustee {idx} partial decrypt = {Di}")

    print()

    # Combine partial decryptions
    M = organizer.combine_decryptions(partials, indices, C2_agg)

    print("Recovered g^sum =", M)
    print()

    print("=== 7. Decode result ===")

    recovered_sum = organizer.decode_result(n, M)

    print("Recovered sum of ratings =", recovered_sum)
    print("Average rating =", recovered_sum / n)


if __name__ == "__main__":
    main()