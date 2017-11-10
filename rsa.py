import random


# Returns all prime numbers from start to stop, inclusive
def find_primes(start, stop):
    if start >= stop:
        print("Invalid range\n")
    primes = [2]
    for n in range(3, stop+1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)
    while len(primes) > 1 and primes[0] < start:
        del primes[0]
    return primes


def relatively_prime(a, b):
    for n in range(2, min(a, b) + 1):
        if a % n == 0 and b % n == 0:
            return False
    return True


def get_bit_length_range(bit_length):
    min = 1 << (bit_length - 1)
    max = (1 << bit_length) - 1
    return min, max


def find_primes_for_bit_length(bit_length):
    n_min, n_max = get_bit_length_range(bit_length)
    primes = find_primes(0, n_max)
    #print primes
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break
    else:
        return 0
    return p, q


def choose_e(order):
    for e in range(3, order, 2):
        if relatively_prime(e, order):
            return e
    else:
        return 0


def choose_d(order, e):
    for d in range(3, order, 2):
        if d * e % order == 1:
            return d
    else:
        return 0

def generate_key_pair(bit_length):
    p, q = find_primes_for_bit_length(bit_length)
    n = p*q
    order = (p-1)*(q-1)
    print((p,q,n))

    e = choose_e(order)
    d = choose_d(order, e)
    return e, d, n


def encrypt(plaintext, e, n):
    return pow(plaintext, e, n)


def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

random.seed(1)
e, d, n = generate_key_pair(18)
print((e, d, n))

# Encrypt ASCII '00'
print(encrypt(12336, e, n))
print(decrypt(encrypt(12336, e, n), d, n))

# Encrypt ASCII '0'
print(encrypt(48, e, n))