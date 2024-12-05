import math
import random

def gcd(a, b):
    """Compute the greatest common divisor (GCD) using the Euclidean algorithm."""
    while b != 0:
        a, b = b, a % b
    return a

def randomized_factoring(n, e, d):
    """
    Perform the randomized factoring algorithm to factor n.
    
    Args:
        n (int): The RSA modulus (public key).
        e (int): The RSA public exponent.
        d (int): The RSA private exponent.
    
    Returns:
        tuple: Factors (p, q) of n.
    """
    k = e * d - 1
    if k % 2 != 0:
        raise ValueError("k is not even, cannot proceed with this method.")
    
    # Decompose k into 2^r * m
    r = 0
    m = k
    while m % 2 == 0:
        m //= 2
        r += 1

    # Perform the randomized trial
    while True:
        a = random.randint(2, n - 2)  # Random integer in [2, n-2]
        x = pow(a, m, n)  # Compute a^m mod n
        if x == 1 or x == n - 1:
            continue

        # Try finding non-trivial roots of 1 mod n
        for _ in range(r - 1):
            prev_x = x
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # Non-trivial factor found
            p = gcd(prev_x - 1, n)
            if p == 1 or p == n:
                continue  # Retry if trivial factor
            q = n // p
            return p, q

# Inputs
n = 1501
e = 323
d = 539

# Factorize n
p, q = randomized_factoring(n, e, d)

# Ensure factors are valid
if p * q != n:
    raise ValueError("Failed to factorize n correctly.")
print(f"Factors of n: p = {p}, q = {q}")

# Compute phi(n)
phi_n = (p - 1) * (q - 1)
print(f"phi(n) = {phi_n}")

# Verify ed ≡ 1 mod phi(n)
verification = (e * d) % phi_n
print(f"Verification: ed = {verification} mod phi(n)")
