import hashlib

class HashingUtility:
    def __init__(self, secret_key: str = ""):
        self.secret_key = secret_key or ""

    def hash_data(self, data: str) -> str:
        # Combine the plaintext data with the secret key
        salted_data = data + self.secret_key
        return hashlib.sha256(salted_data.encode()).hexdigest()
