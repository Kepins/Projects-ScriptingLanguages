import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from password_manager.encryption.exceptions import DecryptionException


def _get_key(password: str) -> bytes:
    # Create PBKDF2HMAC object with SHA-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"random salt",
        iterations=1337,
        backend=default_backend()
    )

    # Derive the key
    return kdf.derive(password.encode('utf-8'))


def encrypt_data(password: str, data: bytes) -> bytes:
    # Derive the key
    key = _get_key(password)

    # Generate a random initialization vector
    iv = os.urandom(16)

    # Create AES cipher object with GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())

    # Create encryptor
    encryptor = cipher.encryptor()

    # Encrypt the message
    ciphertext = encryptor.update(data) + encryptor.finalize()

    # Get the authentication tag
    tag = encryptor.tag

    return iv + ciphertext + tag


def decrypt_data(password: str, encrypted_bytes: bytes) -> bytes:
    # Derive the key
    key = _get_key(password)

    if len(encrypted_bytes) < 32:
        raise DecryptionException()

    # Separate IV, ciphertext, and authentication tag
    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:-16]
    tag = encrypted_bytes[-16:]

    # Create AES cipher object with GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())

    # Create decryptor
    decryptor = cipher.decryptor()

    try:
        # Decrypt the ciphertext
        data = decryptor.update(ciphertext) + decryptor.finalize()
    except InvalidTag:
        raise DecryptionException()

    return data
