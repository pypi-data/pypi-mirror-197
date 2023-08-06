"""This is module to support encryption."""
import base64
import hashlib

from Cryptodome.Cipher import AES


def encrypt_data(data: str) -> str:
    """Encrypts data using AES.MODE_CBC.

    Args:
        data (str): The data to be encrypted as a bytes object.

    Returns:
        str: The encrypted data as a base64-encoded string.
    """
    iv = b"0123456789abcdef"  # Fixed initialization vector
    new_data = data.encode("utf-8")
    key = hashlib.sha256(b"mysecretkey").digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding_len = AES.block_size - len(data) % AES.block_size
    new_data += bytes([padding_len] * padding_len)
    encrypted = cipher.encrypt(new_data)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts base64-encoded data using AES.MODE_CBC.

    Args:
        encrypted_data (str): The base64-encoded encrypted data.

    Returns:
        str: The decrypted data as a bytes object.
    """
    iv = b"0123456789abcdef"  # Fixed initialization vector
    key = hashlib.sha256(b"mysecretkey").digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = base64.b64decode(encrypted_data.encode("utf-8"))
    decrypted = cipher.decrypt(encrypted)
    padding_len = decrypted[-1]
    return decrypted[:-padding_len].decode("utf-8")
