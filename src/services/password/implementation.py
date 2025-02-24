import hashlib
import os

from src.services.password.constants import HASH_NAME, ITERATIONS


class PasswordService:
    @staticmethod
    def create_hashed_password_and_salt(password: str) -> tuple[str, str]:
        salt = os.urandom(32)
        encoded_password = password.encode("UTF-8")
        key = hashlib.pbkdf2_hmac(HASH_NAME, encoded_password, salt, ITERATIONS)
        return key.hex(), salt.hex()

    @staticmethod
    def verify_password(try_password: str, hashed_password: str, salt: str) -> bool:
        try_password_bytes = try_password.encode("UTF-8")
        salt_bytes = bytes.fromhex(salt)
        try_key = hashlib.pbkdf2_hmac(HASH_NAME, try_password_bytes, salt_bytes, ITERATIONS)
        real_key = bytes.fromhex(hashed_password)
        return try_key == real_key
