from cryptography.fernet import Fernet
from utils.settings import settings

fernet = Fernet(settings.SECRET_KEY.encode())


def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
