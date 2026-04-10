# CLI-PasswordManager
A basic CLI-based password manager that will display simple functions like storing passwords. However, the passwords will be encrypted until the master key is entered.  Once entered, the passwords will be decrypted and displayed. Uses Fernet (AES-128-CBC + HMAC) with PBKDF2 key derivation.
