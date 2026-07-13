from cryptography.fernet import Fernet
import os
def get_fernet():
    key=os.environ.get('ENCRYPTION_KEY')
    return Fernet(key)
def encrypt_token(plaintext):
    f=get_fernet()
    return f.encrypt(plaintext.encode()).decode()
def decrypt_token(ciphertext):
    f=get_fernet()
    return f.decrypt(ciphertext.encode()).decode()