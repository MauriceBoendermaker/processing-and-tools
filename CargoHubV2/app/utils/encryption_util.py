from cryptography.fernet import Fernet

class EncryptionUtility:
    def __init__(self, secret_key: str):
        self.fernet = Fernet(secret_key)

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()
