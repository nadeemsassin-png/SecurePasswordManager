# SecurePasswordManager

A command-line password manager written in Python. Credentials are stored in an encrypted vault protected by a master password.

## Features
- AES-GCM authenticated encryption: a wrong password or a modified vault fails to open
- scrypt key derivation with a random salt
- Commands to create a vault, add, get, list, and delete entries
- Strong password generator

## Install
```bash
git clone https://github.com/nadeemsassin-png/SecurePasswordManager.git
cd SecurePasswordManager
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install cryptography
```

## Usage
```bash
python cli.py init                      # create a new vault
python cli.py add example.com myuser    # add an entry (prompts for the password)
python cli.py get example.com           # show an entry
python cli.py list                      # list all sites
python cli.py delete example.com        # remove an entry
python cli.py generate                  # generate a 20-character password
python cli.py generate --length 32      # choose a custom length
```
Every command except `generate` asks for the master password. The vault is saved as `vault.enc`.

## Security Design
- The master password is never stored. A 32-byte key is derived from it with scrypt and a random 16-byte salt.
- The vault is encrypted with AES-GCM using a random 12-byte nonce. The file on disk is `salt + nonce + ciphertext`.
- GCM authenticates the data, so any change to the file causes decryption to fail.
- Uses the `cryptography` library instead of custom crypto.

## Testing
- **Wrong master password:** decryption fails with "Wrong master password or vault was modified."
- **Tampered vault:** flipped one byte of the encrypted file, then tried the correct password. Decryption still failed, which shows GCM detects modification.
- **CLI:** tested init, add, list, get, and delete, including `get` on a deleted entry (returns "No entry").

## Limitations
- Educational project, not security audited.
- `get` prints the password to the terminal in plain text.
- No protection against malware or a compromised machine.
- A weak master password is still guessable. scrypt only slows attackers down.
- No auto-lock yet.
