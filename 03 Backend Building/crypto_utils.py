import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants for Argon2id (Matching the previous architecture's military-grade specs)
TIME_COST = 3
MEMORY_COST = 65536  # 64 MB
PARALLELISM = 4
HASH_LEN = 32        # 256-bit key for AES

def generate_salt() -> bytes:
    """Generates a random 16-byte salt."""
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a 256-bit key from the password and salt using Argon2id.
    """
    return hash_secret_raw(
        secret=password.encode('utf-8'),
        salt=salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LEN,
        type=Type.ID
    )

def encrypt_data(key: bytes, plaintext_data: bytes) -> tuple[bytes, bytes]:
    """
    Encrypts data using AES-256-GCM.
    Returns: (nonce, ciphertext_with_tag)
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce is standard for GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext_data, None)
    return nonce, ciphertext

def decrypt_data(key: bytes, nonce: bytes, ciphertext_with_tag: bytes) -> bytes:
    """
    Decrypts AES-256-GCM encrypted data.
    """
    aesgcm = AESGCM(key)
    # This will raise InvalidTag if the data was tampered with or password is wrong
    return aesgcm.decrypt(nonce, ciphertext_with_tag, None)
