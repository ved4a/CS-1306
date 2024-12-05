import random

# Function to generate random coefficients for the polynomial
def generate_polynomial(secret, k, prime):
    """
    Generate a random polynomial of degree (k-1) with the constant term as the secret.

    Args:
        secret (int): The secret to be shared.
        k (int): Minimum number of shares required to reconstruct the secret.
        prime (int): A prime number larger than the secret.

    Returns:
        list: Coefficients of the polynomial.
    """
    coefficients = [secret] + [random.randint(0, prime - 1) for _ in range(k - 1)]
    return coefficients

# Function to evaluate the polynomial at a given x
def evaluate_polynomial(coefficients, x, prime):
    """
    Evaluate the polynomial at a specific x value under a prime modulus.

    Args:
        coefficients (list): Coefficients of the polynomial.
        x (int): The x value to evaluate.
        prime (int): A prime number for modular arithmetic.

    Returns:
        int: The result of the polynomial evaluation.
    """
    result = 0
    for i, coeff in enumerate(coefficients):
        result = (result + coeff * (x ** i)) % prime
    return result

# Split the secret into shares
def split_secret(secret, n, k, prime):
    """
    Split a secret into n shares using Shamir's Secret Sharing scheme.

    Args:
        secret (int): The secret to be shared.
        n (int): Total number of shares to generate.
        k (int): Minimum number of shares required to reconstruct the secret.
        prime (int): A prime number larger than the secret.

    Returns:
        list: A list of n shares as (x, y) tuples.
    """
    coefficients = generate_polynomial(secret, k, prime)
    shares = [(x, evaluate_polynomial(coefficients, x, prime)) for x in range(1, n + 1)]
    return shares

# Reconstruct the secret from k shares using Lagrange Interpolation
def reconstruct_secret(shares, prime):
    """
    Reconstruct the secret using k shares.

    Args:
        shares (list): A list of (x, y) tuples.
        prime (int): A prime number for modular arithmetic.

    Returns:
        int: The reconstructed secret.
    """
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator, denominator = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * -xj) % prime
                denominator = (denominator * (xi - xj)) % prime
        lagrange_coefficient = numerator * pow(denominator, -1, prime)
        secret = (secret + yi * lagrange_coefficient) % prime
    return secret

# Add two shares
def add_shares(share1, share2, prime):
    """
    Add two shares together.

    Args:
        share1 (tuple): The first share as (x, y).
        share2 (tuple): The second share as (x, y).
        prime (int): A prime number for modular arithmetic.

    Returns:
        tuple: The resulting share.
    """
    if share1[0] != share2[0]:
        raise ValueError("Shares must have the same x-coordinate to be added.")
    return (share1[0], (share1[1] + share2[1]) % prime)

# Add a public value to a share
def add_public_value(share, value, prime):
    """
    Add a public value to a share.

    Args:
        share (tuple): The share as (x, y).
        value (int): The public value to add.
        prime (int): A prime number for modular arithmetic.

    Returns:
        tuple: The resulting share.
    """
    return (share[0], (share[1] + value) % prime)

# Multiply a share by a public value
def multiply_share(share, value, prime):
    """
    Multiply a share by a public value.

    Args:
        share (tuple): The share as (x, y).
        value (int): The public value to multiply.
        prime (int): A prime number for modular arithmetic.

    Returns:
        tuple: The resulting share.
    """
    return (share[0], (share[1] * value) % prime)

# Demonstration
if __name__ == "__main__":
    secret = 1234
    n = 5
    k = 3
    prime = 2027  # A prime number larger than the secret

    print("Secret:", secret)

    # Split the secret
    shares = split_secret(secret, n, k, prime)
    print("Shares:", shares)

    # Reconstruct the secret from k shares
    reconstructed_secret = reconstruct_secret(shares[:k], prime)
    print("Reconstructed Secret:", reconstructed_secret)

    # Add two shares
    new_share = add_shares(shares[0], shares[1], prime)
    print("Added Shares:", new_share)

    # Add a public value to a share
    public_value = 10
    modified_share = add_public_value(shares[0], public_value, prime)
    print("Share + Public Value:", modified_share)

    # Multiply a share by a public value
    multiplier = 3
    scaled_share = multiply_share(shares[0], multiplier, prime)
    print("Share * Public Value:", scaled_share)
