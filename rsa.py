

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

def encrypt(plaintext, e, n):
    return pow(plaintext, e, n)

def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)


print(encrypt(51, 7, 391))