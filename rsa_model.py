import rsa
import base64

def create_rsa_key():
    (pubkey, prikey) = rsa.newkeys(1024)
    return pubkey, prikey


def encrypt(text, pubkey):
    crypto = rsa.encrypt(text, pubkey)
    return crypto


def decrypt(text, privkey):
    mess = rsa.decrypt(text, privkey).decode()
    return mess

