"""
A basic CLI-based password manager that will display simple functions like storing passwords. However, the passwords will be encrypted until the master key is entered.
 Once entered, the passwords will be decrypted and displayed.   

Uses Fernet (AES-128-CBC + HMAC) with PBKDF2 key derivation
"""

# importing cryptography library, using symmetric encryption like PBK, AES-128, HMAC
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
import getpass
import hashlib


class PasswordManager:
    def __init__(self):
        self.DATA_FILE = 'passwords.enc'
        self.MASTER_HASH_FILE = 'master.hash'
        self.SALT_FILE = 'salt.dat'
        self.passwords = []
        self.master_password = None
        
        # Initialize salt
        if os.path.exists(self.SALT_FILE):
            with open(self.SALT_FILE, 'rb') as f:
                self.salt = f.read()
        else:
            self.salt = os.urandom(16)
            with open(self.SALT_FILE, 'wb') as f:
                f.write(self.salt)
    
    #
    def derive_key(self, master_password):
        """Derive encryption key from master password"""

        """"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), # hash function 
            length=32, # length in bytes , 256 bit key
            salt=self.salt, # salt it
            iterations=100000, 
        )
        # encode it with base 64
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    # hash the password using sha256
    def hash_password(self, password):
        """
            Hash master password
            password.encode changes string into bytes
        """

        return hashlib.pbkdf2_hmac('sha256', password.encode(), self.salt, 100000).hex()
    
    def setup_master_password(self):
        """First time setup"""
        print("\n=== First Time Setup ===")
        while True:
            password = getpass.getpass("Create master password: ")
            
            if len(password) < 6:
                print("Password must be at least 6 characters.")
                continue
            """Ensure the password is correct"""
            confirm = getpass.getpass("Confirm master password: ")
            if password != confirm:
                print("Passwords don't match!")
                continue
            
            with open(self.MASTER_HASH_FILE, 'w') as f:
                f.write(self.hash_password(password))
            print("Master password created!\n")
            return password
    # verify master password function
    def verify_master_password(self):
        """Login with master password"""
        if not os.path.exists(self.MASTER_HASH_FILE):
            return self.setup_master_password()
        
        with open(self.MASTER_HASH_FILE, 'r') as f:
            stored_hash = f.read().strip()

        attempts = 3
        # while loop that will lock after 3 failed attempts
        while attempts > 0:
            password = getpass.getpass("Enter master password: ")
            # hash the input, compare it to the master password hash.
            if self.hash_password(password) == stored_hash:
                return password
            # -1 after every attempt
            attempts -= 1
            if attempts > 0:
                print(f"Incorrect! {attempts} attempts remaining.")
            # too many failed attempts
            else:
                print("Too many failed attempts.")
                exit(1)
    
    # encrypt function
    def encrypt(self, data):
        """Encrypt data"""
        #
        key = self.derive_key(self.master_password)
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data):
        """Decrypt data"""
        key = self.derive_key(self.master_password)
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()
    
    def load_passwords(self):
        """Load passwords from file"""
        if not os.path.exists(self.DATA_FILE):
            self.passwords = []
            return
        
        try:
            with open(self.DATA_FILE, 'r') as f:
                encrypted = f.read()
            decrypted = self.decrypt(encrypted)
            self.passwords = json.loads(decrypted)
        except:
            self.passwords = []
    
    def save_passwords(self):
        """Save passwords to file"""
        data = json.dumps(self.passwords, indent=2)
        encrypted = self.encrypt(data)
        with open(self.DATA_FILE, 'w') as f:
            f.write(encrypted)
    
    def add_password(self):
        """Add new password"""
        print("\n=== Add Password ===")
        website = input("Website: ").strip()
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        
        self.passwords.append({
            'website': website,
            'username': username,
            'password': password
        })
        
        self.save_passwords()
        print("✓ Password saved!\n")
    
    def list_passwords(self):
        """List all passwords"""
        if not self.passwords:
            print("\nNo passwords stored.\n")
            return
        
        print("\n" + "="*60)
        print(f"{'#':<4} {'Website':<20} {'Username':<20} {'Password':<15}")
        print("="*60)
        
        for i, entry in enumerate(self.passwords, 1):
            print(f"{i:<4} {entry['website']:<20} {entry['username']:<20} {entry['password']:<15}")
        
        print("="*60 + "\n")
    
    def delete_password(self):

        self.list_passwords()
        
        if not self.passwords:
            return
        
        try:
            index = int(input("Enter number to delete: "))
            if 1 <= index <= len(self.passwords):
                entry = self.passwords[index - 1]
                confirm = input(f"Delete '{entry['website']}'? (y/n): ")
                
                if confirm.lower() == 'y':
                    del self.passwords[index - 1]
                    self.save_passwords()
                    print("✓ Password deleted!\n")
                else:
                    print("Cancelled.\n")
            else:
                print("Invalid number!\n")
        except:
            print("Invalid input!\n")
    
    def run(self):
        print("\n🔐 Password Manager")
        print("="*60)
        
        # Login
        self.master_password = self.verify_master_password()
        self.load_passwords()
        
        print("\n✓ Unlocked!\n")
        
        # Menu loop
        while True:
            print("1. Add Password")
            print("2. List Passwords")
            print("3. Delete Password")
            print("4. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.add_password()
            elif choice == '2':
                self.list_passwords()
            elif choice == '3':
                self.delete_password()
            elif choice == '4':
                print("\nGoodbye!\n")
                break
            else:
                print("\nInvalid choice!\n")


if __name__ == "__main__":
    try:
        pm = PasswordManager()
        pm.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!\n")
