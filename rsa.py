

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



print(encrypt(51, 7, 391))