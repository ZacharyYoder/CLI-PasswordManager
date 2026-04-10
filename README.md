CLI Password Manager
A command-line password manager built in Python that encrypts stored credentials using industry-standard cryptographic primitives. Developed as a final project for a 300-level Cryptography course.

Features

AES-128-CBC encryption via Fernet for all stored credentials
PBKDF2-HMAC-SHA256 key derivation with 100,000 iterations and random salt generation
Master password authentication with brute-force lockout after 3 failed attempts
Persistent encrypted storage — passwords are never written to disk in plaintext
Secure password entry via getpass (no terminal echo)


How It Works

On first run, a random 16-byte salt is generated and stored locally
The master password is hashed using PBKDF2-HMAC-SHA256 and stored for verification
A separate encryption key is derived from the master password + salt using PBKDF2
All credentials are serialized to JSON, encrypted with Fernet (AES-128-CBC + HMAC), and written to disk
On login, the entered password is hashed and compared — if correct, the encryption key is derived and credentials are decrypted in memory

Usage
bash# Install dependencies
pip install cryptography

# Run
python password_manager.py
Menu Options
1. Add Password    — Store a new credential (encrypted immediately)
2. List Passwords  — Decrypt and display all stored credentials
3. Delete Password — Remove a stored credential
4. Exit

Security Notes

The master password is never stored in plaintext — only its PBKDF2 hash
Encryption key is derived fresh on each session and never persisted
3 failed login attempts triggers an automatic lockout
All file I/O uses encrypted blobs; plaintext only exists in memory during an active session

Technologies Used

Python 3
cryptography library (Fernet, PBKDF2HMAC, hashes)
hashlib, os, json, getpass, base64


Course Context
Built as a final project for a 300-level Cryptography course. Focused on practical application of symmetric encryption, key derivation functions, and secure credential storage patterns.
