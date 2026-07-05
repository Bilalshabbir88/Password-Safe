import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '03 Backend Building'))

from crypto_utils import generate_salt, derive_key, encrypt_data, decrypt_data
from cryptography.exceptions import InvalidTag


def test_generate_salt_length():
    salt = generate_salt()
    assert len(salt) == 16


def test_generate_salt_unique():
    salts = {generate_salt() for _ in range(100)}
    assert len(salts) == 100


def test_derive_key_length():
    salt = generate_salt()
    key = derive_key("testpassword", salt)
    assert len(key) == 32


def test_derive_key_different_salts():
    key1 = derive_key("samepassword", generate_salt())
    key2 = derive_key("samepassword", generate_salt())
    assert key1 != key2


def test_derive_key_different_passwords():
    salt = generate_salt()
    key1 = derive_key("password1", salt)
    key2 = derive_key("password2", salt)
    assert key1 != key2


def test_encrypt_decrypt_roundtrip():
    key = derive_key("testpassword", generate_salt())
    plaintext = b"Hello, CipherVault!"
    nonce, ciphertext = encrypt_data(key, plaintext)
    decrypted = decrypt_data(key, nonce, ciphertext)
    assert decrypted == plaintext


def test_decrypt_wrong_key():
    key = derive_key("correctpassword", generate_salt())
    wrong_key = derive_key("wrongpassword", generate_salt())
    plaintext = b"secret data"
    nonce, ciphertext = encrypt_data(key, plaintext)
    try:
        decrypt_data(wrong_key, nonce, ciphertext)
        assert False, "Should have raised InvalidTag"
    except InvalidTag:
        pass


def test_decrypt_tampered_ciphertext():
    key = derive_key("testpassword", generate_salt())
    plaintext = b"sensitive info"
    nonce, ciphertext = encrypt_data(key, plaintext)
    tampered = bytearray(ciphertext)
    tampered[-1] ^= 0xFF
    try:
        decrypt_data(key, nonce, bytes(tampered))
        assert False, "Should have raised InvalidTag"
    except InvalidTag:
        pass


def test_encrypt_unique_nonces():
    key = derive_key("testpassword", generate_salt())
    plaintext = b"same data"
    nonce1, ct1 = encrypt_data(key, plaintext)
    nonce2, ct2 = encrypt_data(key, plaintext)
    assert nonce1 != nonce2
    assert ct1 != ct2


def test_encrypt_decrypt_empty_data():
    key = derive_key("testpassword", generate_salt())
    nonce, ciphertext = encrypt_data(key, b"")
    decrypted = decrypt_data(key, nonce, ciphertext)
    assert decrypted == b""


def test_encrypt_decrypt_large_data():
    key = derive_key("testpassword", generate_salt())
    plaintext = os.urandom(1024 * 1024)
    nonce, ciphertext = encrypt_data(key, plaintext)
    decrypted = decrypt_data(key, nonce, ciphertext)
    assert decrypted == plaintext
