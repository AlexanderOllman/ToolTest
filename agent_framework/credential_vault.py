import nacl.secret, nacl.pwhash, nacl.utils, json, pathlib, getpass

STORE = pathlib.Path.home() / ".mcp_creds"
STORE.mkdir(exist_ok=True)

SALT_SIZE = nacl.pwhash.argon2id.SALTBYTES
KEY_SIZE = nacl.secret.SecretBox.KEY_SIZE

def _kdf(master: str, salt: bytes) -> bytes:
    return nacl.pwhash.argon2id.kdf(KEY_SIZE, master.encode(), salt,
                                   nacl.pwhash.argon2id.OPSLIMIT_MODERATE,
                                   nacl.pwhash.argon2id.MEMLIMIT_MODERATE)

def save(service: str, secret: dict):
    pw = getpass.getpass(f"Master password for vault (save {service}): ")
    salt = nacl.utils.random(SALT_SIZE)
    box = nacl.secret.SecretBox(_kdf(pw, salt))
    enc = box.encrypt(json.dumps(secret).encode())
    (STORE / f"{service}.vault").write_bytes(salt + enc)


def load(service: str):
    fp = STORE / f"{service}.vault"
    if not fp.exists():
        return None
    raw = fp.read_bytes()
    salt, enc = raw[:SALT_SIZE], raw[SALT_SIZE:]
    pw = getpass.getpass("Master password for vault: ")
    box = nacl.secret.SecretBox(_kdf(pw, salt))
    try:
        dec = box.decrypt(enc)
        return json.loads(dec)
    except Exception:
        return None 