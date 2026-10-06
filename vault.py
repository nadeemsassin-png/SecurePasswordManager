import os, json
from getpass import getpass
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

def derive_key(password, salt):
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(password.encode())

def save_vault(path, password, data):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    ct = AESGCM(key).encrypt(nonce, json.dumps(data).encode(), None)
    with open(path, "wb") as f:
        f.write(salt + nonce + ct)

def load_vault(path, password):
    with open(path, "rb") as f:
        blob = f.read()
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    key = derive_key(password, salt)
    try:
        return json.loads(AESGCM(key).decrypt(nonce, ct, None))
    except InvalidTag:
        raise SystemExit("Wrong master password or vault was modified.")

if __name__ == "__main__":
    pw = getpass("Master password: ")
    save_vault("test.enc", pw, {"example.com": {"user": "nj", "pass": "testpass123"}})
    print(load_vault("test.enc", pw))