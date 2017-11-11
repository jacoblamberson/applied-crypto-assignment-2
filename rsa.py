import random, sys


# Checks to see if a number is likely to be prime.
def is_prime(n):
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert (2 ** s * d == n - 1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n is definitely composite

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True  # no base tested showed n as composite


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


def get_bit_length(n):
    return len(bin(n))-2


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
    #print((p,q,n))

    e = choose_e(order)
    d = choose_d(order, e)
    return e, d, n


def encrypt(plaintext, e, n):
    return pow(plaintext, e, n)


def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

input = ""
output = ""
keyfile = ""
ivfile = ""
public = ""
secret = ""
numBit = ""
checkiv = 0

for a in range(1, len(sys.argv)):
    if sys.argv[a] == "-k":
        keyfile = sys.argv[a + 1]
    if sys.argv[a] == "-p":
        pubKey = sys.argv[a + 1]
    if sys.argv[a] == "-o":
        output = sys.argv[a + 1]
    if sys.argv[a] == "-i":
        input = sys.argv[a + 1]
    if sys.argv[a] == "-s":
        secret = sys.argv[a + 1]
    if sys.argv[a] == "-n":
        numBit = sys.argv[a + 1]
    if sys.argv[a] == "-f":
        function = sys.argv[a + 1]

infile = open(input, "rb")
hex_data = infile.read()
infile.close()

outfile = open(output, "wb")

pubFile = open(pubKey, "wb")

secretFile = open(secret, "wb")

keyring = open(keyfile, "r")
key = keyring.read()
hex_data = binascii.hexlify(hex_data).decode('utf-8')



def get_random_bits(n):
    # THIS IS NOT SECURE RANDOMNESS, but I need determinism. Sorry not sorry.
    return random.getrandbits(n)


def get_r(n):
    sr = ""
    while len(sr) < n/4:
        tmp = int(get_random_bits(8))
        if tmp != 0:
            tmps = format(tmp, 'x')
            if len(tmps) == 1:
                tmps = '0' + tmps
            sr += tmps
    r = int(sr, 16)
    r = r & int('1' * n, 2)
    return r


def construct_element_pkcs(m, N):
    n = get_bit_length(N)
    r_bit_length = n // 2
    m_bit_length = n // 2 - 24
    r = get_r(r_bit_length)

    element = m
    element = element ^ (r << (8 + m_bit_length))
    element = element ^ (2 << (r_bit_length + 8 + m_bit_length))

    return element


def deconstruct_element_pkcs(element, N):
    n = get_bit_length(N)
    m_bit_length = n // 2 - 24
    m = element & int('1' * m_bit_length, 2)
    return m


def construct_element(m, N):
    n = get_bit_length(N)
    r_bit_length = n // 2
    m_bit_length = n // 2
    r = get_r(r_bit_length)

    element = m
    element = element ^ (r << m_bit_length)

    return element


def deconstruct_element(element, N):
    n = get_bit_length(N)
    m_bit_length = n // 2
    m = element & int('1' * m_bit_length, 2)
    return m


def pad_and_encrypt(m, e, N):
    element = construct_element(m, N)
    ciphertext = encrypt(element, e, N)
    return ciphertext


def decrypt_and_unpad(ciphertext, d, N):
    element = decrypt(ciphertext, d, N)
    plaintext = deconstruct_element(element, N)
    return plaintext



input = ""
output = ""
keyfile = ""
public = ""
secret = ""
numBit = ""
function = ""

for a in range(1, len(sys.argv)):
    if sys.argv[a] == "-k":
        keyfile = sys.argv[a + 1]
    if sys.argv[a] == "-p":
        public = sys.argv[a + 1]
    if sys.argv[a] == "-o":
        output = sys.argv[a + 1]
    if sys.argv[a] == "-i":
        input = sys.argv[a + 1]
    if sys.argv[a] == "-s":
        secret = sys.argv[a + 1]
    if sys.argv[a] == "-n":
        numBit = sys.argv[a + 1]
    if sys.argv[a] == "-f":
        function = sys.argv[a + 1]


if function == 'encrypt':
    keyring = open(keyfile, "r")
    keylist = keyring.readlines()
    keyring.close()
    infile = open(input, "r")
    inlist = infile.readlines()
    infile.close()
    n = int(keylist[0])
    N = int(keylist[1])
    e = int(keylist[2])
    plaintext = int(inlist[0])
    ciphertext = pad_and_encrypt(plaintext, e, N)
    outfile = open(output, "w")
    outfile.write(str(ciphertext) + '\n')
    outfile.close()
elif function == 'decrypt':
    keyring = open(keyfile, "r")
    keylist = keyring.readlines()
    keyring.close()
    infile = open(input, "r")
    inlist = infile.readlines()
    infile.close()
    n = int(keylist[0])
    N = int(keylist[1])
    d = int(keylist[2])
    ciphertext = int(inlist[0])
    plaintext = decrypt_and_unpad(ciphertext, d, N)
    outfile = open(output, "w")
    outfile.write(str(plaintext) + '\n')
    outfile.close()
elif function == 'keygen':
    n = int(numBit)
    e, d, N = generate_key_pair(n)
    sfile = open(secret, "w")
    sfile.write(str(n) + '\n')
    sfile.write(str(N) + '\n')
    sfile.write(str(d) + '\n')
    sfile.close()
    pfile = open(public, "w")
    pfile.write(str(n) + '\n')
    pfile.write(str(N) + '\n')
    pfile.write(str(e) + '\n')
    pfile.close()
else:
    print("BAD INPUT PANIC!!!")



exit()

random.seed(1337)
e, d, N = generate_key_pair(13)
print((e, d, N))

# Encrypt ASCII '00'
print(encrypt(12336, e, N))
print(decrypt(encrypt(12336, e, N), d, N))

# Encrypt ASCII '0'
print(encrypt(48, e, N))

print(get_bit_length(7))
tmp = get_r(256)
print(tmp)
print(format(tmp, 'x'))
print(format(tmp << 8*2, 'x'))
print(format(construct_element(int('beef', 16), int('1000000000000', 16)), 'x'))
#print(get_bit_length(10000000000000000000000000))
print(format(279936, 'x'))
